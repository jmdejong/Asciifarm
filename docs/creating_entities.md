
# Creating Entities

## Normal entity creation

### Location

To create an entity for in the game you should add a factory function for that entity to the `asciifarm.server.gameobjects.entities` dict.

The best place to define this is in one of the modules in `asciifarm.server.gameobjects`.
`base.py` is for all ground and ground-like stuff; most of the other modules should be self-describing.
`misc.py` is for everything that does not fit in another catagory.

All dictionary indices must be unique.
Though the definitions are in different modules, the actual dictionary is flat and not nested.

### Example

**OUTDATED**: components will work differently

This is an example for putting an entity factory function in the entity dict.

    entities["pebble"] = 
      lambda:
        Entity(
          sprite="pebble",
          height=0.2,
          components={
            "item": Item(),
            "serialize": Static("pebble")})

### Explanation

Each entry in the entity dict must be a function that returns an Entity instance.
Lambda functions are usually used for simplicity, but this is not necessary.
