
from ..system import system
from ..datacomponents import Trap, Fighter, EnterMessage

@system([EnterMessage, Trap, Fighter])
def trap(obj, roomData, messages, trap, fighter):
    for message in messages:
        fighter.target = message.actor

