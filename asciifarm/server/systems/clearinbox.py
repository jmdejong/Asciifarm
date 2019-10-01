
from ..datacomponents import Message


def clearinbox(roomData):
    for compt, entities in roomData.dataComponents.items():
        if issubclass(compt, Message):
            for entity in entities:
                del entity.dataComponents[compt]
            roomData.dataComponents[compt] = set()
