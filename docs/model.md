
# Game Model

The model is the part of the code that handles all game logic.

Outside code will send input to the model and call update on it in a given interval.
No part in the model has references to anything outside the model (except possibly callbacks/event listeners).

In the code, the model is represented by the World class.
Other important parts of the model are Player, Room, RoomData, GroundPatch, Entity and all components.


## World class

The World class is the main handle of the model to the outside world.

Since most actual logic happens in the Rooms, this class is mainly for keeping track of them and the Players

## Room class

Rooms contain a part of the world, and are actually a model in themselves.
