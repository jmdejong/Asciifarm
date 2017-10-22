# rooms

This is a multiplayer ascii game (or so far, only the framework for a game actually)

The goal now is to have players walk around in different rooms where they can interact with things.

A lot of functionality is actually working.

## Working Features

- Multiplayer
- Walking around
- Switching between rooms
- Persistent inventory
- Fighting 
- NPC's
- Farming

## Installation/starting instructions

Requires python3, tested to work on at least python 3.5.2 in linux

Because of the use of NCURSES and Unix Domain Sockets, it probably won't work on windows (will be fixed later)

Not tested on mac. If anyone could test this for me this would be much appreciated.

Run `hostrooms.py` from the same directory to start the server.

Run `rooms` or `playgame.py` to start the client

## Playing instructions

Use the arrow keys or wasd to move around.
Use 'g' to add an item from the ground into your inventory.
Use 'q' to drop the top item in your inventory.
Use 'e' to use/interact with the top item in your inventory.
Use 'F' to attack an enemy in the same square as you.
Use WASD to attack enemies in adjacent squares.


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
- test server robustness
- nondeterminism in combat and grow times
- more content (rooms, objects etc)
- equipment
- configurable keybindings
- better reaction on player death
- room unloading when there are no players
- better interaction selection
- write converter to convert tiled map files to readable files
- configurable graphics
- multicharacter sprites in client
- in-game chat
- multiple socket types (regular unix, abstract unix, inet and websocket), selectable as command line arguments

## DONE

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
