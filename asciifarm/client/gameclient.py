#! /usr/bin/python3

import os
import sys

import threading
import json
import getpass
import argparse
import string
from queue import Queue


from .inputhandler import InputHandler

class Client:
    
    def __init__(self, stdscr, display, name, connection, keybindings, logFile=None):
        self.stdscr = stdscr
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
        
    
    def send(self, data):
        text = json.dumps(data)
        self.connection.send(text)
    
    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.getInput, daemon=True).start()
        
        self.connection.send(json.dumps(["name", self.name]))
        self.command_loop()
    
    def listen(self):
        self.connection.listen(self.pushMessage, self.onConnectionError)
    
    def pushMessage(self, databytes):
        self.queue.put(("message", databytes))
    
    def onConnectionError(self, error):
        self.queue.put(("error", error))
    
    def getInput(self):
        while True:
            key = self.stdscr.getch()
            self.queue.put(("input", key))
    
    def close(self, msg=None):
        self.keepalive = False
        self.closeMessage = msg
    
    
    def update(self, databytes):
        if len(databytes) == 0:
            self.close("Connection closed by server")
            return
        datastr = databytes.decode('utf-8')
        data = json.loads(datastr)
        if len(data) and isinstance(data[0], str):
            data = [data]
        for msg in data:
            msgType = msg[0]
            if msgType == 'error':
                error = msg[1]
                if error == "nametaken":
                    self.close("error: name is already taken")
                    return
                if error == "invalidname":
                    self.close("error: "+ msg[2])
                    return
                self.log(error)
            if msgType == 'field':
                field = msg[1]
                fieldWidth = field['width']
                fieldHeight = field['height']
                self.display.resizeField((fieldWidth, fieldHeight))
                fieldCells = field['field']
                mapping = field['mapping']
                self.display.drawFieldCells(
                    (tuple(reversed(divmod(i, fieldWidth))),
                     mapping[spr])
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
                self.log(*msg[1:])
            if msgType == "options":
                if msg[1] != None:
                    description, options = msg[1]
                    self.log(description)
                    for option in options:
                        self.log(option)
        
        self.display.update()
    
    def log(self, text, type=None):
        if not isinstance(text, str):
            text = str(text)
        self.display.addMessage(text, type)
        if self.logFile:
            with(open(self.logFile, 'a')) as f:
                f.write("[{}] {}\n".format(type or "", text))
    
    
    def command_loop(self):
        while self.keepalive:
            action = self.queue.get()
            if action[0] == "message":
                self.update(action[1])
            elif action[0] == "input":
                self.inputHandler.onInput(action[1])
            elif action[0] == "error":
                raise action[1]
            else:
                raise Exception("invalid action in queue")
    



