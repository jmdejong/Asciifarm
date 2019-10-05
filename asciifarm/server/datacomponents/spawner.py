
class Spawner:
    
    def __init__(self, spawned, number=1, setHome=False):
        self.spawned = spawned
        self.number = number
        class MySquad:
            pass
        self.squad = MySquad
        self.setHome = setHome
