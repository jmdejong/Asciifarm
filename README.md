# AsciiFarm

Formerly: **Rooms** 

This is a multiplayer ascii farming/fighting game.

![screenshot](screenshot.png)
<!-- why doesn't the screenshot get updated? -->

## Working Features

- Multiplayer
- Walking around
- Switching between rooms
- Persistent inventory
- Fighting 
- NPC's
- Farming
- Building

## Installation/starting instructions

Requires python3, tested to work on at least python 3.5.2 in linux

Because of the use of NCURSES, it probably won't work on windows (will be fixed later)

Not tested on mac. If anyone could test this for me this would be much appreciated.

Not on pypi yet, but you should be able to install it like this:

    python -m pip install git+https://github.com/jmdejong/Asciifarm.git

Then you can run `hostfarm` to start the server and `asciifarm` to play the
game!

## Playing instructions

Use the arrow keys or wasd to move around.
Use 'e' to add an item from the ground into your inventory.
Use 'q' to drop the top item in your inventory.
Use 'E' to use/interact with the top item in your inventory.
Use 'f' interact with something in the same square as you.
Use 'F' to attack an enemy in the same square as you.
Use WASD to attack enemies in adjacent squares.


## Development/Hacking

If you want to help us out, great!

These instructions are untested (much has changed since the last tests)

### Pipenv style

If you don't have pipenv yet, go ahead and install it, clone the repo, and
start up a new shell:

    python3 -m pip install pipenv
    git clone https://github.com/jmdejong/Asciifarm.git asciifarm
    cd asciifarm
    pipenv shell --three

Next time you'll just need to `cd asciifarm && pipenv shell`.

### `venv` style

What's that? You can't install pipenv (not even with `--user`)? That's OK, you
can use the built-in virtualenv:

    python3 -m venv ~/.virtualenvs/asciifarm
    source ~/.virtualenvs/asciifarm/bin/activate
    git clone https://github.com/jmdejong/Asciifarm.git asciifarm
    cd asciifarm

### Install asciifarm

Now you can install it:

    python -m pip install -e .

Now `asciifarm` and `hostfarms` should be on your path and you can start up the
game. Cool. :sparkles:


## Vision/ideas

The idea is to make 3 different kind of areas:

- private areas, where players can build their own house/farm
  * these areas will be the only one where players can build
  * other players can only enter with permission of the owner
  * maybe some group areas too? (that can be bought with in-game currency)
- public areas, where players can interact with each other and npcs
  * towns, where players can trade
  * static dungeons, where monsters spawn
  * whatever levels someone feels like making
  * similar to the world of most mmorpgs
- procedurally generated dungeons, where players can explore and fight for loot
  * like roguelikes
  * if the player dies they can not return to the same dungeon
  * group dungeons would be great too

## TODO first

- better code documentation
- testing
- nondeterminism in combat and grow times
- make farming more work
- equipment
- autofight/autoretaliate?
- display target enemy health
- better reaction on player death
- room unloading when there are no players
- better inventory selection
- runtime-created rooms
- in-game chat
- world persistence
- support websockets
- windows comptibility (libtcod/tdl instead of ncurses?)
- write converter to convert tiled map files to readable files

## Other Ideas

- multicharacter sprites
- plants growing as cellular automata

## DONE

- merge package brach
- only plant seeds in soil
- make idle NPC's stay around spawn
- messages in the client
- sort objects on ground on height
- follow player when room larger than terminal
- multiple actions per keypress
- healthbar
- colours
- fullwidth characters as sprites
- load world from files
- more content (rooms, objects etc)
- multiple socket types (regular unix, abstract unix, inet), selectable as command line arguments
- configurable graphics
- configurable keybindings
- make items usable
- farming
- loot
- more efficient target detection for monsters
- more efficient drawing/communication by only updating changed squares
- growing plants
- monster/object spawners
- healing
- make health persistent
- make server robust to invalid messages
- attack cooldown
- add enemies
- factions
- add combat
- improve inventory: probably store it in Player instead of Playerent
- better interaction system
- more code reusability in gameobjects
- avoid long files
