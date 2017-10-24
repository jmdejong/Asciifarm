
# Game Model

The model is the part of the code that handles all game logic.

Outside code will send input to the model and call update on it in a given interval.
No part in the model has references to anything outside the model.

In the code, the model is represented by the World class.
Other important parts of the model are Player, Room, RoomData, GroundPatch, Entity and all components.


## World class

The World class is the main handle of the model to the outside world.

Since most actual logic happens in the Rooms, this class is mainly for keeping track of them and the Players

## Room class

Rooms contain a part of the world, and are actually a model in themselves.


## Player class 

The purpose of the player class is to keep a handle to the player entity that can be used by outside functions, and to keep the player data persistent between when the player leaves a room (either to go to another room, or because the player disconnected.
