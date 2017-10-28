#!/usr/bin/python3 -u



import sys

if sys.version_info[0] < 3:
    print("This game is written in python 3.\nRun 'python3 "+sys.argv[0]+"' or './"+sys.argv[0]+"'")
    sys.exit(-1)

from server import main

main()
