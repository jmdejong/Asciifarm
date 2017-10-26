#! /usr/bin/python3

import os
import sys

import curses
import threading
#import logging
import json
import getpass
import argparse
from .display.screen import Screen
import string
from .display import Display


#logging.basicConfig(filename="client.log", filemode='w', level=logging.DEBUG)


class Client:
    
    def __init__(self, stdscr, name, connection, keybindings, characters):
        self.stdscr = stdscr
        self.screen = Screen(stdscr)
        
        self.name = name
        
        self.keepalive = True
        
        self.connection = connection
        
        
        self.commands = {ord(key): command for key, command in keybindings['input'].items()}
        
        self.controlsString = "Controls:\n"+'\n'.join(
                chr(key) + ": " + ' '.join(action)
                for key, action in self.commands.items()
                if chr(key) in string.printable)
        
        self.connection.send(json.dumps(["name", name]))
        
        
        self.display = Display(self.screen, characters)
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
                fieldWidth = field['width']
                fieldHeight = field['height']
                fieldCells = field['field']
                mapping = field['mapping']
                self.display.drawFieldCells(
                    (tuple(reversed(divmod(i, fieldWidth))),
                     mapping[spr])
                    for i, spr in enumerate(fieldCells))
            
            if msgType == 'changecells'and len(msg[1]):
                self.display.drawFieldCells(msg[1])
            
            if msgType == "health":
                self.display.showHealth(*msg[1])
            if msgType == "inventory":
                self.info["inventory"] = msg[1]
            if msgType == "ground":
                self.info["ground"] = msg[1]
        
        infostring = json.dumps(self.info, indent=2)
        infostring += "\n\n" + self.controlsString
        self.display.showInfo(infostring)
        
        self.display.update()
    
    def command_loop(self):
        while self.keepalive:
            key = self.stdscr.getch()
            if key == 27:
                self.keepalive = False
            if key in self.commands:
                self.connection.send(json.dumps(["input", self.commands[key]]))
    



