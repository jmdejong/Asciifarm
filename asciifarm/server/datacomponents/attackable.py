

class Attackable:
    
    component = "attackable"
    
    def __init__(self, maxHealth, health=None, defence=0, defense=None):
        self.maxHealth = maxHealth
        self.health = health or maxHealth
        if defense is not None:
            defence = defense
        self.defence = defence
        self.attacks = []
    
    def attack(self, strength, attacker):
        self.attacks.append(("attack", strength, attacker))
        
    def heal(self, health, source):
        self.attacks.append(("heal", health, source))
    
    def getHealth(self):
        return (self.health, self.maxHealth)
    
    def healthFull(self):
        return self.health >= self.maxHealth
    
    def isDead(self):
        return self.health <= 0
    


