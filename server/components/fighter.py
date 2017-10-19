

class Fighter:
    
    def __init__(self, health, strength=0):
        self.health = health
        self.strength = strength
    
    def attach(self, owner, events):
        self.owner = owner
    
    def damage(self, damage, attacker):
        self.health -= damage
        
        observable = self.owner.getComponent("observable")
        if observable:
            observable.trigger("damage", attacker, damage)
        
        if self.isDead():
            self.die(attacker)
    
    def attack(self, other):
        otherFighter = other.getComponent("fighter")
        if not otherFighter:
            return
        damage = self.strength
        otherFighter.damage(damage, self.owner)
        
        observable = self.owner.getComponent("observable")
        if observable:
            observable.trigger("attack", other, damage)
            if otherFighter.isDead():
                observable.trigger("kill", other)
    
    def die(self, killer):
        
        observable = self.owner.getComponent("observable")
        if observable:
            observable.trigger("die", killer)
        
        self.owner.remove()
    
    def getHealth(self):
        return self.health
    
    def isDead(self):
        return self.health <= 0


