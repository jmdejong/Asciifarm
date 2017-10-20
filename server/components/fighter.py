
import timeout

class Fighter:
    
    def __init__(self, health, strength=0, slowness=1):
        self.health = health
        self.strength = strength
        self.target = None
        self.slowness = slowness
    
    def attach(self, owner, events):
        self.owner = owner
        self.fightEvent = events["fight"]
        self.timeout = timeout.Timeout(events["update"], self.slowness)
    
    def damage(self, damage, attacker):
        self.health -= damage
        
        observable = self.owner.getComponent("observable")
        if observable:
            observable.trigger("damage", attacker, damage)
        
        if self.isDead():
            self.die(attacker)
    
    def attack(self, other):
        self.target = other
        self.fightEvent.addListener(self.doAttack)
    
    def doAttack(self):
        other = self.target
        if other and self.timeout.isReady():
            otherFighter = other.getComponent("fighter")
            if otherFighter:
                damage = self.strength
                otherFighter.damage(damage, self.owner)
                
                self.timeout.timeout()
                
                observable = self.owner.getComponent("observable")
                if observable:
                    observable.trigger("attack", other, damage)
                    if otherFighter.isDead():
                        observable.trigger("kill", other)
        
        self.target = None
        self.fightEvent.removeListener(self.doAttack)
    
    def die(self, killer):
        
        observable = self.owner.getComponent("observable")
        if observable:
            observable.trigger("die", killer)
        
        self.owner.remove()
    
    
    def getHealth(self):
        return self.health
    
    def isDead(self):
        return self.health <= 0
    
    def remove(self):
        self.fightEvent.removeListener(self.doAttack)
        self.timeout.remove()


