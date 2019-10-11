
import random
import string

class Squad:
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, other):
        return self.name is other.name

class Spawner:
    
    def __init__(self, spawned, number=1, setHome=False, squad=None):
        self.spawned = spawned
        self.number = number
        if squad is None:
            squad = "_" + "".join(random.choices(string.ascii_lowercase, k=20))
        self.squad = squad
        self.setHome = setHome
