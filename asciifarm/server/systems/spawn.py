
from ..system import system
from ..import gameobjects
from ..datacomponents import Spawner, SpawnMessage, Home, Squad

@system([Spawner, SpawnMessage])
def spawn(obj, roomData, spawner, _spawnmessages):
    hasSpawned = 0
    # todo: serialise squad for both spawner and spawned
    for earlierspawn in roomData.getEntities([Squad]):
        squad = roomData.getComponent(earlierspawn, Squad)
        if squad.name == spawner.squad:
            hasSpawned += 1
    
    if hasSpawned < spawner.number:
        spawned = gameobjects.buildEntity(spawner.spawned, roomData)
        roomData.addComponent(spawned, Squad(spawner.squad))
        if spawner.setHome:
            roomData.addComponent(spawned, Home(obj))
        spawned.place(obj.getGround())
    

