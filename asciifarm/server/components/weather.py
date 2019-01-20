

import random

from .component import Component

class Weather(Component):
    
    def __init__(self, speed=1, spread=0, direction="south"):
        self.speed = speed
        self.spread = spread
        self.direction = direction
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData, stamp):
        self.moveEvent = roomData.getEvent("move")
        self.moveEvent.addListener(self.move)
    
    def move(self):
        speed = self.speed
        for i in range(int(speed)):
            self.moveStep()
        if (speed - int(speed)) > random.random():
            self.moveStep()
        if self.spread > random.random():
            self.moveStep(random.choice(["east", "west"]))
    
    def moveStep(self, direction=None):
        if direction is None:
            direction = self.direction
        if self.owner.getGround() is None:
            return
        neighbours = self.owner.getGround().getNeighbours()
        if direction in neighbours:
            newPlace = neighbours[direction]
            self.owner.place(newPlace)
            self.owner.trigger("move")
        else:
            self.owner.remove()
    
    def remove(self):
        self.moveEvent.removeListener(self.move)
            
