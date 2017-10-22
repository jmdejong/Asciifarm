#! /usr/bin/python3

import sys

if sys.version_info[0] < 3:
    print("This game is written in python 3.\nRun 'python3 "+sys.argv[0]+"' or './"+sys.argv[0]+"'")
    sys.exit(-1)

sys.path.append(sys.path[0]+"/client/")
sys.path.append(sys.path[0]+"/shared/")

import argparse
import getpass
import main


parser = argparse.ArgumentParser(description="The client to Rooms. Run this to connect to to the server.", epilog="""
Gameplay information:
    Control your player with the arrow keys or wasd. Press escape to exit.
    You can pick up something with the 'e' key, and drop whatever you're holding with 'q'.
    Currently you can't do much more than walking around and moving stones.

~Troido""", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-n', '--name', help='Your player name (must be unique!). Defaults to username', default=getpass.getuser())
parser.add_argument('-s', '--socket', help='The socket address to connect to. Defaults to \0roomtest\nIf the addres starts with a null byte it is treated as abstract address (usually what you want), Otherwise it is treated as a unix filename', default="\0roomtest")
parser.add_argument('-k', '--keybindings', help='The file with the keybindings', type=argparse.FileType('r'))
parser.add_argument('-c', '--characters', help='The file with the character mappings for the graphics', type=argparse.FileType('r'))
args = parser.parse_args()

main.main(args.name, args.socket, args.keybindings, args.characters)
