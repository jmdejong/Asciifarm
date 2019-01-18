#! /usr/bin/python3


import argparse
import getpass
import json
import os
import os.path

from .start import main as clientmain
#from .paths import keybindingsPath, charmapPath
from . import loaders


#standardCharFiles = [name[:-5] for name in os.listdir(charMapPath) if name[-5:] == ".json"]
#standardKeyFiles = [name[:-5] for name in os.listdir(keybindingsPath) if name[-5:] == ".json"]


defaultAdresses = {
    "abstract": "asciifarm",
    "unix": "asciifarm.socket",
    "inet": "localhost:9021",
    }

def main(argv=None):

    parser = argparse.ArgumentParser(description="The client to AsciiFarm. Run this to connect to to the server.", epilog="""
    Gameplay information:
        Walk around and explore the rooms.
        Kill the goblins and plant the seeds.

    ~troido""", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-n', '--name', help='Your player name (must be unique!). Defaults to username on inet sockets and tildename on (unix socket (including abstract)', default=None)
    parser.add_argument("-a", "--address", help="The address of the socket. When the socket type is 'abstract' this is just a name. When it is 'unix' this is a filename. When it is 'inet' is should be in the format 'address:port', eg 'localhost:8080'. Defaults depends on the socket type")
    parser.add_argument("-s", "--socket", help="the socket type. 'unix' is unix domain sockets, 'abstract' is abstract unix domain sockets and 'inet' is inet sockets. ", choices=["abstract", "unix", "inet"], default="abstract")
    parser.add_argument('-k', '--keybindings', help='The file with the keybinding configuration. This file is a JSON file.', default="default")
    parser.add_argument('-c', '--characters', help='The file with the character mappings for the graphics. If it is either of these names: {} it will be loaded from the charmaps directory.'.format(list(loaders.standardCharFiles.items())), default="default")
    parser.add_argument('-o', '--logfile', help='All game messages will be written to this file.', default=None)
    
    colourGroup = parser.add_mutually_exclusive_group()
    colourGroup.add_argument('-l', '--colours', '--colors', help='enable colours! :)', action="store_true")
    colourGroup.add_argument('-b', '--nocolours', '--nocolors', help='disable colours! :)', action="store_true")
    
    args = parser.parse_args(argv)
    
    charmap = loaders.loadCharmap(args.characters)
    
    keybindings = loaders.loadKeybindings(args.keybindings)
    
    address = args.address
    if address is None:
        address = defaultAdresses[args.socket]
    if args.socket == "abstract":
        address = '\0' + address
    elif args.socket == "inet":
        hostname, sep, port = address.partition(':')
        address = (hostname, int(port))
    
    colours = True
    if args.colours:
        colours = True
    elif args.nocolours:
        colours = False
    
    name = args.name
    if name is None:
        username = getpass.getuser()
        if args.socket == "unix" or args.socket == "abstract":
            name = "~"+username
        else:
            name = username
    
    clientmain(name, args.socket, address, keybindings, charmap, colours, args.logfile)

