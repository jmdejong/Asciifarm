
import re
import unicodedata

class InvalidMessageError(Exception):
    errType = "invalidmessage"
    description = ""
    
    def __init__(self, description="", errType=None):
        self.description = description
        if errType is not None:
            self.errType = errType

class InvalidNameError(InvalidMessageError):
    errType = "invalidname"

class Message:
    
    @classmethod
    def msgType(cls):
        return cls.typename
    
    def to_json(self):
        raise NotImplementedError
    
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
    nameRegex = re.compile("(~|\w)\w*")
    categories = {"Lu", "Ll", "Lt", "Lm", "Lo", "Nd", "Nl", "No", "Pc"}
    
    
    def __init__(self, name):
        assert isinstance(name, str), InvalidNameError("name must be a string")
        assert (len(name) > 0), InvalidNameError("name needs at least one character")
        assert (len(bytes(name, "utf-8")) <= 256), InvalidNameError("name may not be longer than 256 utf8 bytes")
        for char in name if name[0] != "~" else name[1:]:
            category = unicodedata.category(char)
            assert category in self.categories, InvalidNameError("all name caracters must be in these unicode categories: " + "|".join(self.categories) + " (except the tilde in a tildename)")
            
        #assert (name.rfind("~") < 1), InvalidNameError("tilde character may only occur at start of name")
        #assert (self.nameRegex.match(name) is not None), InvalidNameError("name must match the following regex: {}".format(self.nameRegex.pattern))
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



messages = {message.msgType(): message for message in [
    NameMessage,
    InputMessage,
    ChatMessage
]}

