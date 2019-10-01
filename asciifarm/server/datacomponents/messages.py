
from . import DC

class Message(DC):
    allowMultiple = True

class EnterMessage(Message):
    
    def __init__(self, actor):
        self.actor = actor
