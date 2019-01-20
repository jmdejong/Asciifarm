

import random

from .component import Component

class Weather(Component):
    
    def __init__(self, maxspeed=1, minspeed=1, spread=0, direction="south"):
        self.maxspeed = maxspeed
        self.minspeed = minspeed
        self.spread = spread
        self.direction = direction
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData, stamp):
        self.moveEvent = roomData.getEvent("move")
        self.moveEvent.addListener(self.move)
    
    def move(self):
        for i in range(random.randint(self.minspeed, self.maxspeed)):
            self.moveStep()
    
    def moveStep(self):
        if self.owner.getGround() is None:
            return
        neighbours = self.owner.getGround().getNeighbours()
        if self.direction in neighbours:
            newPlace = neighbours[self.direction]
            self.owner.place(newPlace)
            self.owner.trigger("move")
        else:
            self.owner.remove()
    
    def remove(self):
        self.moveEvent.removeListener(self.move)
            
