
from ..datacomponents import Listen

def sound(roomData):
    entities = roomData.getEntities([Listen])
    for entity in entities:
        listen = roomData.getComponent(entity, Listen)
        for sound in roomData.sounds:
            listen.sounds.append(sound)
    for source, text in roomData.sounds:
        print("{}: {}: {}".format(" ", source.getName(), text))
    roomData.sounds = []
