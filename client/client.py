#! /usr/bin/python3

import os
import sys

import curses
import threading
#import logging
import json
import getpass
import argparse
from .screen import Screen
import string

# todo: remove references to tron

#logging.basicConfig(filename="client.log", filemode='w', level=logging.DEBUG)


class Client:
    
    def __init__(self, stdscr, name, connection, keybindings, characters):
        self.stdscr = stdscr
        self.screen = Screen(stdscr)
        
        self.name = name
        
        self.keepalive = True
        
        self.connection = connection
        
        self.lastinfostring = None
        
        self.commands = {ord(key): command for key, command in keybindings['input'].items()}
        
        self.controlsString = "Controls:\n"+'\n'.join(
                chr(key) + ": " + ' '.join(action)
                for key, action in self.commands.items()
                if chr(key) in string.printable)
        
        self.connection.send(json.dumps(["name", name]))
        
        self.fieldWidth = 0
        self.fieldHeight = 0
        
        self.characters = characters["mapping"]
        self.defaultChar = characters.get("default", '?')
        self.charWidth = characters.get("charwidth", 1)
        
        self.info = {}
        
        threading.Thread(target=self.listen, daemon=True).start()
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
            if msgType == 'field':
                field = msg[1]
                self.fieldWidth = field['width']
                self.fieldHeight = field['height']
                fieldCells = field['field']
                mapping = field['mapping']
                self.screen.changeCells((
                        ((i%self.fieldWidth)*self.charWidth, i//self.fieldWidth, self.getChar(mapping[sprite])) 
                        for (i, sprite) in enumerate(fieldCells)
                    ), self.fieldWidth*self.charWidth, self.fieldHeight)
            
            if msgType == 'changecells'and len(msg[1]):
                changedCells = msg[1]
                self.screen.changeCells((
                        (x*self.charWidth, y, self.getChar(sprite)) 
                        for ((x, y), sprite) in changedCells
                    ), self.fieldWidth*self.charWidth, self.fieldHeight)
            
            if msgType == "health":
                self.info["health"] = msg[1]
            if msgType == "inventory":
                self.info["inventory"] = msg[1]
            if msgType == "ground":
                self.info["ground"] = msg[1]
        
        infostring = json.dumps(self.info, indent=2)
        infostring += "\n\n" + self.controlsString
        if infostring != self.lastinfostring:
            self.screen.putPlayers(infostring, self.fieldWidth*self.charWidth+2)
            self.lastinfostring = infostring
        self.screen.refresh()
    
    def getChar(self, sprite):
        char = self.characters.get(sprite, self.defaultChar)
        if isinstance(char, str):
            return char
        return char[0]
    
    def command_loop(self):
        while self.keepalive:
            key = self.stdscr.getch()
            if key == 27:
                self.keepalive = False
            if key in self.commands:
                self.connection.send(json.dumps(["input", self.commands[key]]))
    



