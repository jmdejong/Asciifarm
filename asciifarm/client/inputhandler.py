
import shlex

class InvalidCommandException(Exception):
    pass


class InputHandler:
    
    def __init__(self, client, display, connection):
        self.client = client
        self.display = display
        self.connection = connection
        
        self.commands = {
            "send": self.send,
            "input": self.input,
            "move": self.move,
            "say": self.say,
            "chat": self.chat,
            "log": self.log,
            "do": self.do,
            "runinput": self.runInput,
            "select": self.select,
            "inputwithselected": self.actWithSelected,
            "eval": self.eval,
            "exec": self.exec,
            "scrollchat": self.scrollChat
            }
    
    def execute(self, action):
        if isinstance(action[0], str):
            command = action[0]
            if command in self.commands:
                self.commands[command](*action[1:])
            else:
                raise InvalidCommandException("Invalid command '{}'".format(command))
        else:
            raise Exception("Command should be a string")
            
        
    
    def send(self, data):
        self.client.send(data)
    
    def input(self, action):
        self.send(["input", action])
    
    def move(self, direction):
        self.input(["move", direction])
    
    def say(self, text):
        self.input(["say", text])
    
    def chat(self, text):
        self.send(["chat", text])
    
    def log(self, text):
        self.client.log(text)
    
    def do(self, actions):
        for action in actions:
            self.execute(action)
    
    def runInput(self):
        message = self.display.getString()
        if message:
            if message[0] == '/':
                if message[1] == '/':
                    self.chat(message[1:])
                else:
                    try:
                        self.execute(shlex.split(message[1:]))
                    except InvalidCommandException as e:
                        self.log(", ".join(e.args))
            else:
                self.chat(message)
    
    def select(self, widget, value, relative=False, modular=False):
        self.display.getWidget(widget).select(value, relative, modular)
    
    def actWithSelected(self, action, widget):
        self.input([action, self.display.getWidget(widget).getSelected()])
    
    def eval(self, *texts):
        text = " ".join(texts)
        self.log(eval(text, {"self": self, "client": self.client, "connection": self.connection, "display": self.display}))
    
    def exec(self, *texts):
        text = " ".join(texts)
        exec(text, {"self": self, "client": self.client, "connection": self.connection, "display": self.display})
    
    def scrollChat(self, lines):
        self.display.scrollBack(lines)
    
    
