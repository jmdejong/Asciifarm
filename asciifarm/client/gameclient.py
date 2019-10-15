

import os
import sys

import threading
import json
import getpass
import argparse
import string
from queue import Queue

import ratuil.inputs

from .inputhandler import InputHandler
from asciifarm.common import messages

class Client:
    
    def __init__(self, display, name, connection, keybindings, logFile=None):
        
        self.display = display
        self.name = name
        self.keepalive = True
        self.connection = connection
        self.logFile = logFile
        self.closeMessage = None
        
        self.inputHandler = InputHandler(self, keybindings["actions"])
        
        self.controlsString = keybindings.get("help", "")
        
        self.display.showInfo(self.controlsString)
        self.queue = Queue()
        
    
    def sendMessage(self, message):
        self.connection.send(message.to_json_bytes())
    
    def sendInput(self, inp):
        message = messages.InputMessage(inp)
        self.sendMessage(message)
    
    def sendChat(self, text):
        try:
            self.sendMessage(messages.ChatMessage(text))
        except messages.InvalidMessageError as e:
            self.log(e.description)
    
    def start(self):
        self.sendMessage(messages.NameMessage(self.name))
        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.getInput, daemon=True).start()
        
        self.command_loop()
    
    def listen(self):
        self.connection.listen(self.pushMessage, self.onConnectionError)
    
    def pushMessage(self, databytes):
        self.queue.put(("message", databytes))
    
    def onConnectionError(self, error):
        self.queue.put(("error", error))
    
    def getInput(self):
        while True:
            key = ratuil.inputs.get_key()
            self.queue.put(("input", key))
    
    def close(self, msg=None):
        self.keepalive = False
        self.closeMessage = msg
    
    
    def update(self, databytes):
        if len(databytes) == 0:
            self.close("Connection closed by server")
            return
        datastr = databytes.decode('utf-8')
        msg = json.loads(datastr)
        message = messages.messages[msg[0]].from_json(msg)
        if isinstance(message, messages.ErrorMessage):
            error = message.errType
            if error == "nametaken":
                self.close("error: name is already taken")
                return
            if error == "invalidname":
                self.close("Invalid name error: "+ str(message.description))
                return
            self.log(message.errType + ": " + message.description)
        elif isinstance(message, messages.MessageMessage):
            self.log(message.text, message.type)
        elif isinstance(message, messages.WorldMessage):
            for msg in message.updates:
                self.handleWorldUpdate(msg)
    
    def handleWorldUpdate(self, msg):
        msgType = msg[0]
        if msgType == 'field':
            field = msg[1]
            fieldWidth = field['width']
            fieldHeight = field['height']
            self.display.resizeField((fieldWidth, fieldHeight))
            fieldCells = field['field']
            mapping = field['mapping']
            self.display.drawFieldCells(
                (
                    tuple(reversed(divmod(i, fieldWidth))),
                    mapping[spr]
                )
                for i, spr in enumerate(fieldCells))
        
        if msgType == 'changecells' and len(msg[1]):
            self.display.drawFieldCells(msg[1])
        
        if msgType == "playerpos":
            self.display.setFieldCenter(msg[1])
        
        if msgType == "health":
            health, maxHealth = msg[1]
            self.display.setHealth(health, maxHealth)
            if maxHealth is None:
                self.log("You have died. Restart the client to respawn")
        if msgType == "inventory":
            self.display.setInventory(msg[1])
        if msgType == "equipment":
            self.display.setEquipment(msg[1])
        if msgType == "ground":
            self.display.setGround(msg[1])
        if msgType == "message":
            type, text = msg[1][:2]
            self.log(text, type)
        if msgType == "options":
            if msg[1] != None:
                description, options = msg[1]
                self.log(description)
                for option in options:
                    self.log(option)
        
    
    def log(self, text, type=None):
        if not isinstance(text, str):
            text = str(text)
        self.display.addMessage(text, type)
        if self.logFile:
            with(open(self.logFile, 'a')) as f:
                f.write("[{}] {}\n".format(type or "", text))
    
    
    def command_loop(self):
        while self.keepalive:
            self.display.update()
            action = self.queue.get()
            if action[0] == "message":
                self.update(action[1])
            elif action[0] == "input":
                if action[1] == "^C":
                    raise KeyboardInterrupt
                self.inputHandler.onInput(action[1])
            elif action[0] == "error":
                raise action[1]
            elif action[0] == "sigwinch":
                self.display.update_size()
            else:
                raise Exception("invalid action in queue")
    
    def onSigwinch(self, signum, frame):
        self.queue.put(("sigwinch", (signum, frame)))
    



