
import collections
from .dc import DC

class Events(DC):
    
    def __init__(self):
        self.messages = collections.deque()
    
    def add(self, message):
        self.messages.append(message)
