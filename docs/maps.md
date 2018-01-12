# Maps

The pregenerated maps are stored as a simple JSON format.
All files should be UTF-8 encoded.

## Main entry

There is one main entry file for the world.
Currently this is 'world.json'.

It has a property called "rooms", which is a dictionary of maps.
The keys are the names of the maps, and the values are the file paths, starting from the directory of the main entry file.

There is another property called "begin" which is the room where the players will spawn by default.

Example:

    {
        "begin": "begin",
        "rooms": {
            "begin": "begin.json",
            "basement": "basement.json"
        }
    }
    

## Room files

The map file has the following properties:

### "width" and "height"

The width and height of the map. Both must be positive integers.

### "spawn"

An array of 2 integers, being the x and y coordinates of the spawnpoint respectively.
The spawnpoint is where the players will appear in the map when not more information about the map is given

### "places"

A dictionary of named places.
The key of the dictionary is the name of the place.
The value is an array of 2 integers, representing the x and y coordinate respectively.

Often, when referring to a certain place the name can be substituted for the coordinates.
This is useful for example when teleporting to a certain point, or when entering the map at a certain point

### "grid"

A list of strings.
The length of the list should be the room height.
The length of each of the strings should be the room width.

Each character in the strings represents one square of the room.
It can contain zero or more objects.

It should be possible to use any unicode character, though it is advised to use only characters of the same width.

### "mapping"

This property is a dictionary to map the characters in the grid to game entities.
The keys in the dictionary are single characters corresponding to the characters in the grid.
The values are either a string, an object (dictionary), or a list of strings and/or dictionaries

If the value is a string, then [server.gameobjects.makeEntity](../asciifarm/server/gameobjects.py) gets called with the this name as objecttype, the roomData and no further arguments.

If the value is an object (which is the same as a dictionary in json) it should have a "type" property and optionally an "args" property and/or a "kwargs" property.
If "args" is set it should be a list, and if "kwargs" is set it should be a dictionary.
"type" selects the object you want to make, and "args" and "kwargs" are the arguments passed to the entity factory in [gameobjects.py](../asciifarm/server/gameobjects.py)

If the value is a list, than it's elements should be either of the above two (or a combination, or just empty).
In fact, all values that are not a list will get converted into a singleton list when parsing.

Example:

    {
        "width": 10,
        "height": 10,
        "spawn": [7, 2],
        "places": {
            "stairup": [2, 7]
        },
        "grid": [
            "          ",
            " ######## ",
            " #......# ",
            " #.o....# ",
            " #......# ",
            " #...o..# ",
            " #.g....# ",
            " #<..^..# ",
            " ######## ",
            "          "
        ],
        "mapping": {
            "o": ["ground", "stone"],
            "#": "wall",
            ".": "ground",
            "^": ["spiketrap"],
            "<": [{
                "type": "roomexit",
                "args": ["begin", "stairdown"],
                "kwargs": {"sprite": "stairup", "size": 1}
            }, "floor"],
            "g": [
                "ground", 
                {
                    "type": "spawner",
                    "args": ["goblin", 2, 50, "portal", "goblinspawner", 1, true, true]
                }
            ],
            " ": []
        }
    }


