
## TODO

- unify object creation
- write howto for entity creation
- reconsider getters and setters
- log chat messages separately server-side
- show ground permissions
- trading
- currency?
- authentication
- labels
- make farming more work
- more crops
- better reaction on player death
- display target enemy health
- better code documentation
- testing
- support websockets
- write converter to convert tiled map files to readable files

## Other Ideas

- multicharacter sprites
- plants growing as cellular automata

## See github issues

- windows comptibility (libtcod/tdl instead of ncurses?)
- player-owned doors (and items)
- different messages for in-game log, let client construct them
- chat colours
- show adjacent objects
- have a difference between ground-like items and interesting items
- tilled soil
- tutorial room

## DONE

- store non-unique and stateless objects as string
- custom getstr
- runtime-created rooms
- autofight/autoretaliate
- red background flash when attacked
- document map format
- world chat
- chat scrolling
- refactor display
- typable commands
- fix window resizing
- transparent background on sprites
- list scrolling (inventory, ground, equipment)
- display equipment
- better inventory selection
- in-game chat
- relative position room transitions
- custom world persistence (json)
- defense/armour
- nondeterminism in combat, grow times and spawn times
- equipment
- world persistence
- log messages in client to file
- room unloading when there are no players
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
