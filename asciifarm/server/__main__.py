#!/usr/bin/python3 -u



import sys

if sys.version_info[0] < 3:
    print("This game is written in python 3.\nRun 'python3 "+sys.argv[0]+"' or './"+sys.argv[0]+"'")
    sys.exit(-1)

if __package__:
    from . import main
else:
    import os.path
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from server import main

main.main()
