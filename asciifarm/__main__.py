
""" This module is kind of a launcher for either the client or the server.
It is recommended not to use this, but instead run `python asciifarm.server` or `python asciifarm.client`.
"""

import sys

# start the server or the client depending on the first command line argument
if len(sys.argv)>1 and sys.argv[1] in {"server", "client"}:
    if __package__:
        if sys.argv[1] == "server":
            from .server import main
        else:
            from .client import main
    else:
        # make it work even if it wasn't executed as module
        import os.path
        sys.path.append(os.path.join(os.path.dirname(__file__)))
        if sys.argv[1] == "server":
            from server import main
        else:
            from client import main
    
    main.main(sys.argv[2:])
else:
    print("Error, first argument should be either 'client' or 'server'", file=sys.stderr)
