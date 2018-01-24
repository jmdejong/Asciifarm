from .. import timeout
from asciifarm.common import utils
import random
from .component import Component
from .. import gameobjects

class Fighter(Component):
    
    def __init__(self, maxHealth, strength=0, slowness=1, health=None, defense=0):
        self.maxHealth = maxHealth
        self.health = health or maxHealth
        self.strength = strength
        self.target = None
        self.slowness = slowness
        self.canAttack = True
        self.defense = defense
    
    def attach(self, obj):
        self.owner = obj
        obj.addListener("roomjoin", self.roomJoin)
    
    def roomJoin(self, o, roomData):
        self.roomData = roomData
        self.fightEvent = roomData.getEvent("fight")
        self.updateEvent = roomData.getEvent("update")
        self.timeout = timeout.Timeout(roomData.getEvent("update"), self.slowness)
    
    def damage(self, damage, attacker):
        self.health -= damage
        self.health = utils.clamp(self.health, 0, self.maxHealth)
        
        # should this be it's own component? ('bleeding' for example)
        if damage > 0 and self.owner.getGround() is not None:
            obj = gameobjects.makeEntity("wound", self.roomData, 4, self.owner.getHeight() - 0.01)
            obj.place(self.owner.getGround())
        
        self.owner.trigger("damage" if damage >= 0 else "heal", attacker, abs(damage))
        
        if self.isDead():
            self.die(attacker)
    
    def attack(self, other):
        self.target = other
        self.fightEvent.addListener(self.doAttack)
    
    def doAttack(self):
        other = self.target
        if other and other.hasComponent("fighter") and self.canAttack:
            otherFighter = other.getComponent("fighter")
            if otherFighter:
                strength = self.getStrength()
                defense = otherFighter.getDefense()
                damage = random.randint(0, int(100*strength / (defense + 100)))
                otherFighter.damage(damage, self.owner)
                
                self.canAttack = False
                self.timeout = timeout.Timeout(self.updateEvent, self.slowness, self.makeReady)
                
                self.owner.trigger("attack", other, damage)
                if otherFighter.isDead():
                    self.owner.trigger("kill", other)
        
        self.target = None
        self.fightEvent.removeListener(self.doAttack)
    
    def die(self, killer):
        
        self.owner.trigger("die", killer)
        
        self.owner.remove()
    
    def getStrength(self):
        strength = self.strength
        if self.owner.hasComponent("equipment"):
            strength += self.owner.getComponent("equipment").getBonus("strength")
        return strength
    
    
    def getDefense(self):
        defense = self.defense
        if self.owner.hasComponent("equipment"):
            defense += self.owner.getComponent("equipment").getBonus("defense")
        return defense
    
    def getHealth(self):
        return (self.health, self.maxHealth)
    
    def healthFull(self):
        return self.health >= self.maxHealth
    
    def heal(self, health, source):
        self.damage(-health, source)
    
    def isDead(self):
        return self.health <= 0
    
    def remove(self):
        self.fightEvent.removeListener(self.doAttack)
        self.timeout and self.timeout.remove()
        obj.removeListener("roomjoin", self.roomJoin)
    
    
    def makeReady(self, to):
        self.canAttack = True
        self.timeout = None
    
    def toJSON(self):
        return {
            "maxHealth": self.maxHealth,
            "strength": self.strength,
            "slowness": self.slowness,
            "health": self.health,
            "defense": self.defense
        }
    


