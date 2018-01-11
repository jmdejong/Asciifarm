
import argparse
import os.path

from . import game
from . import loader


defaultAdresses = {
    "abstract": "asciifarm",
    "unix": "asciifarm.socket",
    "inet": "localhost:9021",
}


thisPath = os.path.dirname(__file__)
farmsPath = os.path.join(thisPath, "..")

defaultWorld = os.path.join(farmsPath, "maps", "world.json")
defaultSaveDir = os.path.join(farmsPath, "saves")

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help="The address of the socket. When the socket type is 'abstract' this is just a name. When it is 'unix' this is a filename. When it is 'inet' is should be in the format 'address:port', eg 'localhost:8080'. Defaults depends on the socket type")
    parser.add_argument("-s", "--socket", help="the socket type. 'unix' is unix domain sockets, 'abstract' is abstract unix domain sockets and 'inet' is inet sockets. ", choices=["abstract", "unix", "inet"], default="abstract")
    loadGroup = parser.add_mutually_exclusive_group()
    loadGroup.add_argument("-w", "--world", help="A json file to load the world from.", default=defaultWorld)
    loadGroup.add_argument("-l", "--load", help="A save file to load the world from", default=defaultSaveDir)
    parser.add_argument("-e", "--savedir", help="Directory to save the world to periodically", default=defaultSaveDir)
    
    args = parser.parse_args(argv)
    address = args.address
    if address is None:
        address = defaultAdresses[args.socket]
    if args.socket == "abstract":
        address = '\0' + address
    elif args.socket == "inet":
        hostname, sep, port = address.partition(':')
        address = (hostname, int(port))
    
    worldData = loader.loadWorld(args.world)
    game.Game(args.socket, worldData, args.load, args.savedir, 1200).start(address)
