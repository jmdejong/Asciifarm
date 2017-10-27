#!/usr/bin/env python3

import sys
import subprocess

if sys.version_info[0] < 3:
    sys.exit('asciifarm currently only supports python3. Try `python3 {}`'.format(' '.join(sys.argv)))

# Munge the path if we're called without `-m`
if not __package__:
    import pathlib
    sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

import argparse
import getpass
import json
import os
import os.path

from textwrap import dedent

from asciifarm import client


thisPath = os.path.dirname(__file__)
charMapPath = os.path.join(thisPath, "charmaps")
keybindingsPath = os.path.join(thisPath, "keybindings")

standardCharFiles = [name[:-5] for name in os.listdir(charMapPath) if name[-5:] == ".json"]
standardKeyFiles = [name[:-5] for name in os.listdir(keybindingsPath) if name[-5:] == ".json"]


default_addresses = {
    "abstract": "asciifarm",
    "unix": "asciifarm.socket",
    "inet": "localhost:9021",
}

def main():
    parser = argparse.ArgumentParser(
        description="The asciifarm client and server."
                    " Run client --help or server --help for more help",
    )
    subparser = parser.add_subparsers(dest='command')
    client_parser = subparser.add_parser(
        'client',
        epilog=dedent(
            """
            Gameplay information:
                Walk around and explore the rooms.
                Kill the goblins and plant the seeds.

            ~troido
            """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    server_parser = subparser.add_parser('server')

    for p in client_parser, server_parser:
        p.add_argument("-a", "--address",
            help="""
                The address of the socket.
                When the socket type is 'abstract' this is just a name.
                When it is 'unix' this is a filename.
                When it is 'inet' is should be in the format 
                'address:port', eg 'localhost:8080'.
                Defaults depends on the socket type
            """)
        p.add_argument("-s", "--socket",
            help="""
                The socket type. 'unix' is unix domain sockets,
                'abstract' is abstract unix domain sockets
                and 'inet' is inet sockets.
            """,
            choices=["abstract", "unix", "inet"],
            default="abstract",
        )

    client_parser.add_argument('-n', '--name',
        help='Your player name (must be unique!). Defaults to username',
        default=getpass.getuser(),
    )
    client_parser.add_argument('-k', '--keybindings',
        help='''
            The file with the keybindings.
            If it is either of these names: {} it will be 
            loaded from the keybindings directory.
        '''.format(standardKeyFiles),
        default="default",
    )
    client_parser.add_argument('-c', '--characters', 
        help='''
            The file with the character mappings for the graphics.
            If it is either of these names: {} it will be loaded 
            from the charmaps directory.
        '''.format(standardCharFiles),
        default="default",
    )
    client_parser.add_argument('-l', '--colours', '--colors',
        help='Use ANSI color escape sequences',
        action="store_true",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    address = args.address or default_addresses[args.socket]
    if args.socket == "abstract":
        address = '\0' + address
    elif args.socket == "inet":
        hostname, port = address.split(':')
        address = (hostname, int(port))

    if args.command == 'client':
        charFile = args.characters
        if args.characters in standardCharFiles:
            charFile = os.path.join(charMapPath, args.characters + ".json")
        with open(charFile, 'r') as cf:
            charMap = json.load(cf)

        keyFile = args.keybindings
        if keyFile in standardKeyFiles:
            keyFile = os.path.join(keybindingsPath, keyFile + ".json")
        with open(keyFile, 'r') as kf:
            keybindings = json.load(kf)
        
        client.main(args.name, args.socket, address, keybindings, charMap, args.colours)
    elif args.command == 'server':
        args = parser.parse_args()
        
        worldData = loader.loadWorld(args.world)
        mainloop.Game(args.socket, worldData).start(address)


if __name__ == '__main__':
    main()
