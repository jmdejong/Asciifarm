#! /usr/bin/python3


import sys

if sys.version_info[0] < 3:
    print("This game is written in python 3.\nRun 'python3 "+sys.argv[0]+"' or './"+sys.argv[0]+"'")
    sys.exit(-1)

sys.path.append(sys.path[0]+"/server/")
sys.path.append(sys.path[0]+"/shared/")
import mainloop
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--socket', help="""
The address of the socket.\n
If this starts with a null byte, it is an abstract socket (this is usually what you want).\n
Otherwise it is a unix file (which you could give permissions)\n
Defaults to \\0roomtest\n
\n
When using a file as socket you will have to remove the file manually after execution (it is suggested to make it in /tmp)""", default="\0roomtest")
args = parser.parse_args()

mainloop.Game().start(args.socket)
