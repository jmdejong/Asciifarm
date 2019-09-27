
import re
import unicodedata
import json

class InvalidMessageError(Exception):
    errType = "invalidmessage"
    description = ""
    
    def __init__(self, description="", errType=None):
        self.description = description
        if errType is not None:
            self.errType = errType
    
    def toMessage(self):
        return ErrorMessage(self.errType, self.description)

class InvalidNameError(InvalidMessageError):
    errType = "invalidname"

class Message:
    
    @classmethod
    def msgType(cls):
        return cls.typename
    
    def to_json(self):
        raise NotImplementedError
    
    def to_json_bytes(self):
        return bytes(json.dumps(self.to_json()), "utf-8")
    
    @classmethod
    def from_json(cls, jsonobj):
        raise NotImplementedError

class ClientToServerMessage(Message):
    
    def body(self):
        raise NotImplementedError
    
    def to_json(self):
        return [self.typename, self.body()]
    
    @classmethod
    def from_json(cls, jsonlist):
        assert len(jsonlist) == 2, InvalidMessageError
        typename, body = jsonlist
        assert typename == cls.msgType(), InvalidMessageError
        return cls(body)
        

class NameMessage(ClientToServerMessage):
    
    typename = "name"
    categories = {"Lu", "Ll", "Lt", "Lm", "Lo", "Nd", "Nl", "No", "Pc"}
    
    
    def __init__(self, name):
        assert isinstance(name, str), InvalidNameError("name must be a string")
        assert (len(name) > 0), InvalidNameError("name needs at least one character")
        assert (len(bytes(name, "utf-8")) <= 256), InvalidNameError("name may not be longer than 256 utf8 bytes")
        if name[0] != "~":
            for char in name:
                category = unicodedata.category(char)
                assert category in self.categories, InvalidNameError("all name caracters must be in these unicode categories: " + "|".join(self.categories) + " (except for tildenames)")
        self.name = name
    
    def body(self):
        return self.name
        
        
class InputMessage(ClientToServerMessage):
    
    typename = "input"
    
    def __init__(self, inp):
        self.inp = inp
    
    def body(self):
        return self.inp

class ChatMessage(ClientToServerMessage):
    
    typename = "chat"
    
    def __init__(self, text):
        assert isinstance(text, str), InvalidMessageError("chat message must be a string")
        assert text.isprintable(), InvalidMessageError("chat messages may only contain printable unicode characters")
        self.text = text
    
    def body(self):
        return self.text



class ServerToClientMessage(Message):
    msglen = 0
    
    
    @classmethod
    def from_json(cls, jsonlist):
        assert len(jsonlist) == cls.msglen, InvalidMessageError
        assert jsonlist[0] == cls.msgType(), InvalidMessageError
        return cls(*jsonlist[1:])


class MessageMessage(ServerToClientMessage): # this name feels stupid
    """ A message to inform the client. This is meant to be read by the user"""
    
    typename = "message"
    msglen = 3
    
    def __init__(self, text, type=""):
        self.text = text
        self.type = type
    
    def to_json(self):
        return [self.typename, self.text, self.type]
    

class WorldMessage(ServerToClientMessage):
    """ A message about the world state """
    
    typename = "world"
    msglen = 2
    
    def __init__(self, updates):
        assert isinstance(updates, list), InvalidMessageError
        self.updates = updates
    
    def to_json(self):
        return [self.typename, self.updates]

class ErrorMessage(ServerToClientMessage):
    
    typename = "error"
    msglen = 3
    
    def __init__(self, errType, description=""):
        self.errType = errType
        self.description = description
    
    def to_json(self):
        return [self.typename, self.errType, self.description]



messages = {message.msgType(): message for message in [
    NameMessage,
    InputMessage,
    ChatMessage,
    WorldMessage,
    ErrorMessage,
    MessageMessage
]}

