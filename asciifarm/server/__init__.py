
import argparse
import pathlib

from server import mainloop
from server import loader


defaultAdresses = {
    "abstract": "asciifarm",
    "unix": "asciifarm.socket",
    "inet": "localhost:9021",
}
default_world = pathlib.Path(__file__).parent.parent.joinpath('maps', 'world.json')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help="The address of the socket. When the socket type is 'abstract' this is just a name. When it is 'unix' this is a filename. When it is 'inet' is should be in the format 'address:port', eg 'localhost:8080'. Defaults depends on the socket type")
    parser.add_argument("-s", "--socket", help="the socket type. 'unix' is unix domain sockets, 'abstract' is abstract unix domain sockets and 'inet' is inet sockets. ", choices=["abstract", "unix", "inet"], default="abstract")
    parser.add_argument("-w", "--world", help="A file to load the world from.", default=str(default_world))  # str is only needed for python 3.5<
    
    args = parser.parse_args()
    address = args.address
    if address == None:
        address = defaultAdresses[args.socket]
    if args.socket == "abstract":
        address = '\0' + address
    elif args.socket == "inet":
        hostname, sep, port = address.partition(':')
        address = (hostname, int(port))
    
    worldData = loader.loadWorld(args.world)
    mainloop.Game(args.socket, worldData).start(address)
