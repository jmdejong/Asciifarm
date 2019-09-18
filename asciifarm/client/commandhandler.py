
import json

try:
    import hy
except ImportError as e:
    hy = None
    hyErr = e

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
            #"inputwithselected": self.actWithSelected,
            "use": self.useSelected,
            "unuse": self.unUseSelected,
            "take": self.takeSelected,
            "eval": self.eval,
            "exec": self.exec,
            "scrollchat": self.scrollChat,
            "json": self.json,
            "j": self.json,
            "ijson": self.ijson,
            "ij": self.ijson,
            "hy": self.hy
        }
        
        self.evalArgs = {
            "self": self,
            "client": self.client,
            "connection": self.client.connection,
            "display": self.client.display,
            "print": self.log
        }
    
    def execute(self, action):
        if action is None:
            return
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
        self.client.display.selectMenu(value, relative, modular)
    
    def selectItem(self, value, relative=False, modular=False):
        self.client.display.selectItem(None, value, relative, modular)
    
    #def actWithSelected(self, action, widget):
        #self.input([action, self.client.display.getWidget(widget).getSelected()])
    
    def useSelected(self):
        menu = self.client.display.getSelectedMenu()
        selected = self.client.display.getSelectedItem(menu)
        if menu in ("inventory", "equipment"):
            action = "use"
        elif menu == "ground":
            action = "interact",
        else:
            return
        self.input([action, selected])
    
    def unUseSelected(self):
        menu = self.client.display.getSelectedMenu()
        selected = self.client.display.getSelectedItem(menu)
        if menu == "inventory":
            action = "drop"
        elif menu == "equipment":
            action = "unequip"
        else:
            return
        self.input([action, selected])
    
    def takeSelected(self):
        menu = self.client.display.getSelectedMenu()
        selected = self.client.display.getSelectedItem(menu)
        if menu == "ground":
            action = "take"
        else:
            return
        self.input([action, selected])
    
    def eval(self, text):
        self.log(eval(text, self.evalArgs))
    
    def exec(self, text):
        exec(text, self.evalArgs)
    
    def hy(self, code):
        if hy is None:
            self.log(hyErr)
            return
        expr = hy.read_str(code)
        self.log(hy.eval(expr, self.evalArgs))
    
    def scrollChat(self, lines):
        self.client.display.scrollBack(lines)
    
    def json(self, text):
        self.execute(json.loads(text))
    
    def ijson(self, text):
        self.input(json.loads(text))
    
    
