#!/usr/bin/python3 -u


import sys

if sys.version_info[0] < 3:
    print("This game is written in python 3.\nRun 'python3 "+sys.argv[0]+"' or './"+sys.argv[0]+"'")
    sys.exit(-1)

sys.path.append(sys.path[0]+"/server/")
import mainloop
import argparse


defaultAdresses = {
    "abstract": "asciifarm",
    "unix": "./asciifarm.socket",
    "inet": "localhost:9021",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help="The address of the socket. When the socket type is 'abstract' this is just a name. When it is 'unix' this is a filename. When it is 'inet' is should be in the format 'address:port', eg 'localhost:8080'. Defaults depends on the socket type")
    parser.add_argument("-s", "--socket", help="the socket type. 'unix' is unix domain sockets, 'abstract' is abstract unix domain sockets and 'inet' is inet sockets. ", choices=["abstract", "unix", "inet"], default="abstract")
    
    args = parser.parse_args()
    address = args.address
    if address == None:
        address = defaultAdresses[args.socket]
    if args.socket == "abstract":
        address = '\0' + address
    elif args.socket == "inet":
        hostname, sep, port = address.partition(':')
        address = (hostname, int(port))
    mainloop.Game(args.socket).start(address)

main()
