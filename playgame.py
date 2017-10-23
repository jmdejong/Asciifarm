#! /usr/bin/python3

import sys

if sys.version_info[0] < 3:
    print("This game is written in python 3.\nRun 'python3 "+sys.argv[0]+"' or './"+sys.argv[0]+"'")
    sys.exit(-1)

sys.path.append(sys.path[0]+"/client/")

import argparse
import getpass
import main


parser = argparse.ArgumentParser(description="The client to AsciiFarm. Run this to connect to to the server.", epilog="""
Gameplay information:
    Control your player with the arrow keys or wasd. Press escape to exit.
    You can pick up something with the 'e' key, and drop whatever you're holding with 'q'.
    Currently you can't do much more than walking around and moving stones.

~Troido""", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-n', '--name', help='Your player name (must be unique!). Defaults to username', default=getpass.getuser())
parser.add_argument("-a", "--address", help="The address of the socket. When the socket type is 'abstract' this is just a name. When it is 'unix' this is a filename. When it is 'inet' is should be in the format 'address:port', eg 'localhost:8080'. Defaults depends on the socket type")
parser.add_argument("-s", "--socket", help="the socket type. 'unix' is unix domain sockets, 'abstract' is abstract unix domain sockets and 'inet' is inet sockets. ", choices=["abstract", "unix", "inet"], default="abstract")
parser.add_argument('-k', '--keybindings', help='The file with the keybindings', type=argparse.FileType('r'))
parser.add_argument('-c', '--characters', help='The file with the character mappings for the graphics', type=argparse.FileType('r'))
args = parser.parse_args()

main.main(args.name, args.socket, args.address, args.keybindings, args.characters)
