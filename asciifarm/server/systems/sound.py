
from ..datacomponents import Listen

def sound(roomData):
    entities = roomData.getEntities([Listen])
    for entity in entities:
        listen = roomData.getComponent(entity, Listen)
        for sound in roomData.sounds:
            listen.notifications.append(sound)
    for sound in roomData.sounds:
        print("{}: {}: {}".format(" ", sound.source, sound.text))
    roomData.sounds = []
