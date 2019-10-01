
from ..datacomponents import Message


def clearinbox(roomData):
    for compt, entities in roomData.dataComponents.items():
        if issubclass(compt, Message):
            roomData.clearComponent(compt)
