
import shlex
import json

class InvalidCommandException(Exception):
    pass


class CommandHandler:
    
    def __init__(self, client):
        self.client = client
        
        self.commands = {
            "send": self.send,
            "input": self.input,
            "move": self.move,
            "say": self.say,
            "pick": self.pick,
            "chat": self.chat,
            "log": self.log,
            "do": self.do,
            "runinput": self.runInput,
            "selectwidget": self.selectWidget,
            "selectitem": self.selectItem,
            "inputwithselected": self.actWithSelected,
            "use": self.useSelected,
            "unuse": self.unUseSelected,
            "take": self.takeSelected,
            "eval": self.eval,
            "exec": self.exec,
            "scrollchat": self.scrollChat,
            "json": self.json,
            "ijson": self.ijson
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
    
    
    # Commands
    
    def send(self, data):
        self.client.send(data)
    
    def input(self, action):
        self.send(["input", action])
    
    def move(self, direction):
        self.input(["move", direction])
    
    def say(self, text):
        self.input(["say", text])
    
    def pick(self, option):
        self.input(["pick", option])
    
    def chat(self, text):
        self.send(["chat", text])
    
    
    def log(self, text):
        self.client.log(text)
    
    def do(self, actions):
        for action in actions:
            self.execute(action)
    
    def runInput(self, startText=""):
        self.client.inputHandler.startTyping(startText)
    
    def selectWidget(self, value, relative=False, modular=False):
        self.client.display.getWidget("switch").select(value, relative, modular)
    
    def selectItem(self, value, relative=False, modular=False):
        self.client.display.getWidget("switch").getSelectedItem().getImpl().select(value, relative, modular)
    
    def actWithSelected(self, action, widget):
        self.input([action, self.client.display.getWidget(widget).getSelected()])
    
    def useSelected(self):
        widget = self.client.display.getWidget("switch").getSelectedItem()
        selected = widget.getImpl().getSelected()
        if widget.name in ("inventory", "equipment"):
            action = "use"
        elif widget.name == "ground":
            action = "interact",
        else:
            return
        self.input([action, selected])
    
    def unUseSelected(self):
        widget = self.client.display.getWidget("switch").getSelectedItem()
        selected = widget.getImpl().getSelected()
        if widget.name == "inventory":
            action = "drop"
        elif widget.name == "equipment":
            action = "unequip"
        else:
            return
        self.input([action, selected])
    
    def takeSelected(self):
        widget = self.client.display.getWidget("switch").getSelectedItem()
        selected = widget.getImpl().getSelected()
        if widget.name == "ground":
            action = "take"
        else:
            return
        self.input([action, selected])
    
    def eval(self, *texts):
        text = " ".join(texts)
        self.log(eval(text, {"self": self, "client": self.client, "connection": self.client.connection, "display": self.client.display}))
    
    def exec(self, *texts):
        text = " ".join(texts)
        exec(text, {"self": self, "client": self.client, "connection": self.client.connection, "display": self.client.display})
    
    def scrollChat(self, lines):
        self.client.display.scrollBack(lines)
    
    def json(self, text):
        self.send(json.loads(text))
    
    def ijson(self, text):
        self.input(json.loads(text))
    
    
