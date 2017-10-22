#! /usr/bin/python3

import os
import sys

import curses
import threading
#import logging
import json
import getpass
import argparse
from connection import Connection
from screen import Screen
import string

# todo: remove references to tron

#logging.basicConfig(filename="client.log", filemode='w', level=logging.DEBUG)


class Client:
    
    def __init__(self, stdscr, name, connection, spectate=False):
        self.stdscr = stdscr
        self.screen = Screen(stdscr)
        
        self.name = name
        
        self.keepalive = True
        
        self.connection = connection
        
        self.lastoutputstring = None
        self.lastinfostring = None
        
        self.commands = {
            ord("w"): ("move", "north"),
            curses.KEY_UP: ("move", "north"),
            ord("s"): ("move", "south"),
            curses.KEY_DOWN: ("move", "south"),
            ord("d"): ("move", "east"),
            curses.KEY_RIGHT: ("move", "east"),
            ord("a"): ("move", "west"),
            curses.KEY_LEFT: ("move", "west"),
            ord("g"): ("take",),
            ord("q"): ("drop",),
            ord("F"): ("attack",),
            ord("W"): ("attack", "north"),
            ord("S"): ("attack", "south"),
            ord("D"): ("attack", "east"),
            ord("A"): ("attack", "west"),
            ord("e"): ("use",),
            ord("f"): ("interact",)
        }
        
        if not spectate:
            self.connection.send(json.dumps({"name":name}))
        
        self.fieldWidth = 0
        self.fieldHeight = 0
        
        fname = os.path.join(os.path.dirname(__file__), "characters.json")
        with open(fname) as f:
            self.characters = json.load(f)['ascii']
        
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
            #print(mapping['0'])
            outputstring = '\n'.join(
                ''.join(
                    self.characters.get(mapping[fieldCells[x + y*self.fieldWidth]], '?') for x in range(self.fieldWidth)
                    ) for y in range(self.fieldHeight)
                )
            if outputstring != self.lastoutputstring:
                self.screen.put(outputstring, self.fieldWidth, self.fieldHeight)
                self.lastoutputstring = outputstring
        
        if 'changecells' in data and len(data['changecells']):
            self.screen.changeCells((
                    (x, y, self.characters.get(sprite, '?')) 
                    for ((x, y), sprite) in data['changecells']
                ), self.fieldWidth, self.fieldHeight)
        
        if 'info' in data:
            infostring = json.dumps(data['info'], indent=2)
            infostring += "\n\n" + self.getControlsString()
            if infostring != self.lastinfostring:
                self.screen.putPlayers(infostring, self.fieldWidth+2)
                self.lastinfostring = infostring
        self.screen.refresh()
    
    def command_loop(self):
        while self.keepalive:
            key = self.stdscr.getch()
            if key == 27:
                self.keepalive = False
            if key in self.commands:
                self.connection.send(json.dumps({"input": self.commands[key]}))
    
    def getControlsString(self):
        return "Controls:\n"+'\n'.join(
            chr(key) + ": " + ' '.join(action)
            for key, action in self.commands.items()
            if chr(key) in string.printable)


def main(name, address, spectate=False):
    
    connection = Connection()
    try:
        connection.connect(address)
    except ConnectionRefusedError:
        print("ERROR: Could not connect to server.\nAre you sure that the server is running and that you're connecting to the right address?", file=sys.stderr)
        return
    
    caught_ctrl_c = False
    def start(stdscr):
        nonlocal caught_ctrl_c
        try:
            client = Client(stdscr, name, connection, spectate)
        except KeyboardInterrupt:
            caught_ctrl_c = True
    
    curses.wrapper(start)
    
    if caught_ctrl_c:
        print('^C caught, goodbye!')


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='Your player name (must be unique!). Defaults to username', default=getpass.getuser())
    parser.add_argument('-s', '--socket', help='The socket file to connect to. Defaults to /tmp/tron_socket', default="/tmp/tron_socket")
    parser.add_argument('-p', '--spectate', help='Join as spectator', action="store_true")
    args = parser.parse_args()
    
    main(args.name, args.socket, args.spectate)

