
# Communication

This document is to descrive how the communication between the server and the client currently works.

There may be better ways and it may be subject to change, but this works now.

## packets over TCP

The communication happens over a TCP Unix Domain Socket, by default an abstract UDS.

In order to send discrete messages (instead of just a stream of bytes) over TCP the message is prefixed by a header of 4 bytes defining the length of the message in big endian notation.
This length is the length of the message body, the header is not included
Both server and client use tcommunicate.py to achieve this.


## JSON data

The message body is JSON text

The top-level JSON value is always a dictionary.
This dict can contain several messages of different types.

For example, if the message is like this:

    {
      "field": <something>
      "info": <something>
    }

Then this should actually be treated as two independent messages: one of type "field" and the other of type "info"


## Client to server messages

Currently there are two types of messages that the client can send to the server: 'name' and 'input'

### 'name' messages

The 'name' message is used to pick the name of a player to connect to.
The value of this message is a string.
This message must be sent before any other communication.

Example message: `{"name": "troido"}`

If a player with that name did not exist yet, it will be created and the connection will be connecte that player.

If a player with that name does exist, but it no other connection is currenty connected to that player, the connection will be connected to that player too.

Once the connection is connected to a player it will put the player in the game and send its view to the player

If another connection is already connected to a player with that name, the server will send an error message and ignore all communication until the next 'name' message.

### 'input' messages

'input' messages are sent to control the player.
If the connection is not connected to any player, these messages are ignored.
The value of this message is a list with a length of at least 1.
The first item in the list is the type of command, later items are arguments

Example message: `{"input": ["move", "east"]}`


## Server to client messages

There are 3 types of messages that the server can send to the client: 'field', 'info' and 'error'

Currently, 'field' and 'info' messages are always sent in the same dictionary, together with a 'type' value.
The 'type' can be ignored and will probably soon be removed

### 'error' messages

'error' messages are sent when a player tries to connect with a name that is already connected or when the input is wrong.
Wrong input is not always guaranteed to give an error message. The value is a string to give the type of error.

Example message: `{"error": "nametaken"}


### 'field' messages

'field' messages send the full visible state of the room
It has the following properties:

- width: the width of the room
- height: the height of the room
- field: a 1 dimensional array (length: width*height) of integers representing the sprites in all cells of the room.
- mapping: an array or dictionary of spritenames. The values in field are the indices for the mapping.

Only one sprite per cell is sent: the one with the larges height.

Example message:

    {"field":
        "width": 3,
        "height": 3,
        "field": [0,0,1,0,0,2,1,0,0],
        "mapping": ["grass", "stone", "player"]
    }

When the character for grass is ',', for stone is 'o' and for player is '@', then this message would correspond to the field:

    ,,o
    ,,@
    o,,

See view.py and Grid.toDict in grid.py for the implementation.


### 'info' messages

'info' messages are used to send information about the player to the server.
Currently the information includes the inventory, the health of the player and the objects on the same cell as the player.

Example message:
    "info": {
        "health": 95,
        "inventory": ["stone", "pebble"],
        "ground": ["grass1"]
    }

See view.py for the implementation.

# Suggested improvements

## partial field update

Sending the complete field each update is very costly for both the client and the server

A solution would be to send a list of areas to be updated (after the player has entered the room initially).

Another solution is to send a list of single cells to be updated.

This improvement has highest priority

## Lists as outer objects

Currently all messages are dictionaries, which results in nonintuitive code where the key determines the type of the message, and where unrelated messages can be send in the same message.

A solution would be to send lists as outer objects where the first element of the list is the type of message.

Example: `["input", ["move", "north"]]`

## Human readable error messages

Currently error messages only have a computer readable string.

It would be nice if it could sent a human readable string too.

This has low priority and is only useful once the client has some console to print to.


