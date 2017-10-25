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
        
        self.lastoutputstring = None
        self.lastinfostring = None
        
        self.commands = {ord(key): command for key, command in keybindings['input'].items()}
        
        self.controlsString = "Controls:\n"+'\n'.join(
                chr(key) + ": " + ' '.join(action)
                for key, action in self.commands.items()
                if chr(key) in string.printable)
        
        self.connection.send(json.dumps({"name": name}))
        
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
        if 'error' in data:
            if data['error'] == "nametaken":
                print("error: name is already taken", file=sys.stderr)
                self.close()
        if 'field' in data:
            self.fieldWidth = data['field']['width']
            self.fieldHeight = data['field']['height']
            fieldCells = data['field']['field']
            mapping = data['field']['mapping']
            outputstring = '\n'.join(
                ''.join(
                    self.characters.get(mapping[fieldCells[x + y*self.fieldWidth]], self.defaultChar) for x in range(self.fieldWidth)
                    ) for y in range(self.fieldHeight)
                )
            if outputstring != self.lastoutputstring:
                self.screen.put(outputstring, self.fieldWidth*self.charWidth, self.fieldHeight)
                self.lastoutputstring = outputstring
        
        if 'changecells' in data and len(data['changecells']):
            self.screen.changeCells((
                    (x*self.charWidth, y, self.characters.get(sprite, self.defaultChar)) 
                    for ((x, y), sprite) in data['changecells']
                ), self.fieldWidth*self.charWidth, self.fieldHeight)
        
        if "health" in data:
            self.info["health"] = data["health"]
        if "inventory" in data:
            self.info["inventory"] = data["inventory"]
        if "ground" in data:
            self.info["ground"] = data["ground"]
        infostring = json.dumps(self.info, indent=2)
        infostring += "\n\n" + self.controlsString
        if infostring != self.lastinfostring:
            self.screen.putPlayers(infostring, self.fieldWidth*self.charWidth+2)
            self.lastinfostring = infostring
        self.screen.refresh()
    
    def command_loop(self):
        while self.keepalive:
            key = self.stdscr.getch()
            if key == 27:
                self.keepalive = False
            if key in self.commands:
                self.connection.send(json.dumps({"input": self.commands[key]}))
    



