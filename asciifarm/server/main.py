
import argparse
import os.path
import signal
from . import game


signal.signal(signal.SIGINT, signal.default_int_handler)


defaultAdresses = {
    "abstract": "asciifarm",
    "unix": "asciifarm.socket",
    "inet": "localhost:9021"
}


thisPath = os.path.dirname(__file__)
farmsPath = os.path.join(thisPath, "..")

defaultWorld = os.path.join(farmsPath, "maps", "world.json")
defaultSaveDir = os.path.join(farmsPath, "saves")

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--socket", help="the socket type and adress. For the type: 'unix' is unix domain sockets, 'abstract' is abstract unix domain sockets and 'inet' is inet sockets. Unix sockets should have a filename as address, abstract sockets just a string and inet sockets should be in the format 'hostname:port'", nargs=2, action="append")
    loadGroup = parser.add_mutually_exclusive_group()
    loadGroup.add_argument("-w", "--world", help="A json file to load the world from.", default=defaultWorld)
    parser.add_argument("-e", "--savedir", help="Directory to save the world to periodically", default=defaultSaveDir)
    
    args = parser.parse_args(argv)
    socketargs = args.socket
    if socketargs is None:
        socketargs = []
    if len(socketargs) == 0:
        socketargs.append(["abstract", "asciifarm"])
    
    sockets = []
    for socktype, address in socketargs:
        assert socktype in ["abstract", "unix", "inet"]
        if address is "":
            address = defaultAdresses[socktype]
        if socktype == "abstract":
            address = '\0' + address
        elif socktype == "inet":
            hostname, sep, port = address.partition(':')
            address = (hostname, int(port))
        sockets.append((socktype, address))
    
    game.Game(sockets, args.world, args.savedir, 300).start()
