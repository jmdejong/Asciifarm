#! /usr/bin/python3

import os
import sys

import curses
import threading
import json
import getpass
import argparse
from .display.screen import Screen
import string
from .display.display import Display

from .inputhandler import InputHandler
from .keynames import nameFromKey

class Client:
    
    def __init__(self, stdscr, display, name, connection, keybindings, logFile=None):
        self.stdscr = stdscr
        self.display = display
        self.name = name
        self.keepalive = True
        self.connection = connection
        self.logFile = logFile
        
        self.inputHandler = InputHandler(self, self.display, self.connection)
        self.keybindings = keybindings["actions"]
        
        self.controlsString = keybindings.get("help", "")
        
        self.display.showInfo(self.controlsString)
        
    
    def send(self, data):
        self.connection.send(json.dumps(data))
    
    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()
        self.connection.send(json.dumps(["name", self.name]))
        self.command_loop()
    
    def listen(self):
        self.connection.listen(self.update, self.close)
    
    def close(self, err=None):
        self.keepalive = False
        sys.exit()
    
    
    def update(self, databytes):
        if not self.keepalive:
            sys.exit()
        datastr = databytes.decode('utf-8')
        data = json.loads(datastr)
        if len(data) and isinstance(data[0], str):
            data = [data]
        for msg in data:
            msgType = msg[0]
            if msgType == 'error':
                error = msg[1]
                if error == "nametaken":
                    print("error: name is already taken", file=sys.stderr)
                    self.close()
                    return
                if error == "invalidname":
                    print("error: "+ msg[2], file=sys.stderr)
                    self.close()
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
                health = msg[1]
                if health:
                    self.display.setHealth(*health)
                else:
                    self.log("You have died. Restart the client to respawn")
            if msgType == "inventory":
                self.display.setInventory(msg[1])
            if msgType == "equipment":
                self.display.setEquipment(msg[1])
            if msgType == "ground":
                self.display.setGround(msg[1])
            if msgType == "message":
                self.log(msg[1])
        
        
        self.display.update()
    
    def log(self, text):
        if not isinstance(text, str):
            text = str(text)
        self.display.addMessage(text)
        if self.logFile:
            with(open(self.logFile, 'a')) as f:
                f.write(text+'\n')
    
    def command_loop(self):
        while self.keepalive:
            key = self.stdscr.getch()
            if key == 27:
                self.keepalive = False
                return
            keyName = nameFromKey(key)
            if keyName in self.keybindings:
                self.inputHandler.execute(self.keybindings[keyName])
    



