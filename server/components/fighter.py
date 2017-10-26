
import timeout
import utils

class Fighter:
    
    def __init__(self, maxHealth, strength=0, slowness=1, health=None):
        self.maxHealth = maxHealth
        self.health = health or maxHealth
        self.strength = strength
        self.target = None
        self.slowness = slowness
        self.canAttack = True
    
    def attach(self, owner, roomData):
        self.owner = owner
        self.fightEvent = roomData.getEvent("fight")
        self.updateEvent = roomData.getEvent("update")
        self.timeout = timeout.Timeout(roomData.getEvent("update"), self.slowness)
    
    def damage(self, damage, attacker):
        self.health -= damage
        self.health = utils.clamp(self.health, 0, self.maxHealth)
        
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
                damage = self.strength
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
    
    
    def makeReady(self, to):
        self.canAttack = True
        self.timeout = None


