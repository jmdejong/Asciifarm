

# Installation instructions


## Simple (pip)

Requires python3, tested to work on at least python 3.5.2 in linux

Because of the use of NCURSES, it probably won't work on windows (will be fixed later)

It works on a mac, but when testing abstract domain sockets didn't work.
Use the command line argument `-s inet` for both client and server to run this on a mac.

Not on pypi yet, but you should be able to install it like this:

    python -m pip install git+https://github.com/jmdejong/Asciifarm.git

Then you can run `hostfarm` to start the server and `asciifarm` to play the
game!



## Raw style (no pip)

    git clone https://github.com/jmdejong/Asciifarm.git
    cd asciifarm
    ./hostfarms

And then in another terminal, in the asciifarm directory:

    ./playgame

## Pipenv style

If you don't have pipenv yet, go ahead and install it, clone the repo, and
start up a new shell:

    python3 -m pip install pipenv
    git clone https://github.com/jmdejong/Asciifarm.git asciifarm
    cd asciifarm
    pipenv shell --three

Next time you'll just need to `cd asciifarm && pipenv shell`.

## `venv` style

What's that? You can't install pipenv (not even with `--user`)? That's OK, you
can use the built-in virtualenv:

    python3 -m venv ~/.virtualenvs/asciifarm
    source ~/.virtualenvs/asciifarm/bin/activate
    git clone https://github.com/jmdejong/Asciifarm.git asciifarm
    cd asciifarm

## Install asciifarm

Now you can install it:

    python -m pip install -e .

Now `asciifarm` and `hostfarms` should be on your path and you can start up the
game. Cool. :sparkles:
