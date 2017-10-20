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

## TODO first

- monster/object spawners
- test server robustness
- more efficient detection for monsters
- growing plants
- more content (rooms, objects etc)
- loot
- equipment
- healing
- room unloading when there are no players
- better interaction selection
- more efficient drawing/communication by only updating changed squares
- write converter to convert tiled map files to readable files
- multicharacter sprites in client

## DONE

- make server robust to invalid messages
- attack cooldown
- add enemies
- factions
- add combat
- improve inventory: probably store it in Player instead of Playerent
- better interaction system
- more code reusability in gameobjects
- avoid long files
