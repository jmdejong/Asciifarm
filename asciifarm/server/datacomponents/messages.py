
from . import DC

class Message(DC):
    allowMultiple = True

class EnterMessage(Message):
    
    def __init__(self, actor):
        self.actor = actor


class LootMessage(Message):
    pass

class StartTimer(Message):
    pass

class Create(Message):
    
    def __init__(self, *templates):
        self.templates = templates

class SpawnMessage(Message):
    pass

class EatMessage(Message):
    pass

class UseMessage(Message):
    def __init__(self, actor, parameter=None):
        self.actor = actor
        self.parameter = parameter
