
from ..system import system
from ..import gameobjects
from ..datacomponents import Spawner, SpawnMessage, Home

@system([Spawner, SpawnMessage])
def spawn(obj, roomData, spawner, _spawnmessages):
    if len(roomData.getEntities([spawner.squad])) < spawner.number:
        spawned = gameobjects.buildEntity(spawner.spawned, roomData)
        roomData.addComponent(spawned, spawner.squad)
        if spawner.setHome:
            roomData.addComponent(spawned, Home(obj))
        spawned.place(obj.getGround())
    

