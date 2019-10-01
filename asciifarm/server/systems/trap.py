
from ..system import system
from ..datacomponents import Inbox, Trap, Fighter
from ..messages import EnterMessage

@system([Inbox, Trap, Fighter])
def trap(obj, roomData, inbox, trap, fighter):
    for message in inbox.messages:
        if isinstance(message, EnterMessage):
            fighter.target = message.actor

