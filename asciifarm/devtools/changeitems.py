#!/usr/bin/python3


# changes several items that are being stored as all their properties into item that are just a name
# since the properties are the same anyways


import os
import sys
import json

def writesafe(filename, data, tempname=None):
    if tempname is None:
        tempname = filename + ".tempfile"
    with open(tempname, 'w') as f:
        f.write(data)
    os.rename(tempname, filename)


def main():

    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])
    else :
        os.chdir(os.path.join(os.path.dirname(__file__), "../saves/"))

    playersaves = os.listdir("players/")
    roomsaves = os.listdir("rooms/")
    
    print("change rooms")
    for filename in roomsaves:
        with open(os.path.join("rooms", filename), 'r') as f:
            data = json.load(f)
        replaceroomitems(data)
        writesafe(filename, json.dumps(data))
    print("rooms changed")
    
    print("change player inventories")
    for filename in playersaves:
        with open(os.path.join("players", filename), 'r') as f:
            data = json.load(f)
        replaceplayeritems(data)
        writesafe(filename, json.dumps(data))
    print("players changed")


def replaceroomitems(data):
    changes = data["changes"]
    for place in changes:
        obj = place[1]
        place[1] = replaceobject(obj)

def replaceplayeritems(data):
    inventory = data["inventory"]["items"]
    for i in range(len(inventory)):
        inventory[i] = replaceobject(inventory[i])
    equipment = data["equipment"]
    for k in equipment:
        equipment[k] = replaceobject(equipment[k])


def replaceobject(obj):
    if not isinstance(obj, dict) or "name" not in obj or sprite not in obj:
        return obj
    name = obj["name"]
    sprite = obj["sprite"]
    if name != sprite:
        return
    if name == "food":
        return "food"
    if name == "pebble":
        return "pebble"


if __name__ == "__main__":
    main()
