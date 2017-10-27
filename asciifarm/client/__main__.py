#! /usr/bin/python3

import sys

if sys.version_info[0] < 3:
    print("This game is written in python 3.\nRun 'python3 "+sys.argv[0]+"' or './"+sys.argv[0]+"'")
    sys.exit(-1)

import argparse
import getpass
import json
import os
import os.path

import client

thisPath = os.path.dirname(__file__)
farmsPath = os.path.join(thisPath, "..")
charMapPath = os.path.join(farmsPath, "charmaps")
keybindingsPath = os.path.join(farmsPath, "keybindings")

standardCharFiles = [name[:-5] for name in os.listdir(charMapPath) if name[-5:] == ".json"]
standardKeyFiles = [name[:-5] for name in os.listdir(keybindingsPath) if name[-5:] == ".json"]


defaultAdresses = {
    "abstract": "asciifarm",
    "unix": "asciifarm.socket",
    "inet": "localhost:9021",
    }

def main():

    parser = argparse.ArgumentParser(description="The client to AsciiFarm. Run this to connect to to the server.", epilog="""
    Gameplay information:
        Walk around and explore the rooms.
        Kill the goblins and plant the seeds.

    ~troido""", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-n', '--name', help='Your player name (must be unique!). Defaults to username', default=getpass.getuser())
    parser.add_argument("-a", "--address", help="The address of the socket. When the socket type is 'abstract' this is just a name. When it is 'unix' this is a filename. When it is 'inet' is should be in the format 'address:port', eg 'localhost:8080'. Defaults depends on the socket type")
    parser.add_argument("-s", "--socket", help="the socket type. 'unix' is unix domain sockets, 'abstract' is abstract unix domain sockets and 'inet' is inet sockets. ", choices=["abstract", "unix", "inet"], default="abstract")
    parser.add_argument('-k', '--keybindings', help='The file with the keybindings. If it is either of these names: {} it will be loaded from the keybindings directory.'.format(standardKeyFiles), default="default")
    parser.add_argument('-c', '--characters', help='The file with the character mappings for the graphics. If it is either of these names: {} it will be loaded from the charmaps directory.'.format(standardCharFiles), default="default")
    
    colourGroup = parser.add_mutually_exclusive_group()
    colourGroup.add_argument('-l', '--colours', '--colors', help='enable colours! :)', action="store_true")
    colourGroup.add_argument('-b', '--nocolours', '--nocolors', help='disable colours! :)', action="store_true")
    args = parser.parse_args()
    
    charFile = args.characters
    if charFile in standardCharFiles:
        charFile = os.path.join(charMapPath, charFile + ".json")
    with open(charFile, 'r') as cf:
        charMap = json.load(cf)
    keyFile = args.keybindings
    if keyFile in standardKeyFiles:
        keyFile = os.path.join(keybindingsPath, keyFile + ".json")
    with open(keyFile, 'r') as kf:
        keybindings = json.load(kf)
    
    address = args.address
    if address == None:
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
    
    client.main(args.name, args.socket, address, keybindings, charMap, colours)

main()
