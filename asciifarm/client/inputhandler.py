
import curses
import curses.ascii

from .commandhandler import CommandHandler, InvalidCommandException
from .keynames import nameFromKey


class InputHandler:
    
    def __init__(self, client, keybindings):
        self.client = client
        self.keybindings = keybindings
        self.commandHandler = CommandHandler(self.client)
        
        self.typing = False
        self.string = ""
        self.cursor = 0
    
    
    def onInput(self, key):
        if not self.typing:
            keyName = nameFromKey(key)
            if keyName in self.keybindings:
                self.commandHandler.execute(self.keybindings[keyName])
        else:
            self.addKey(key)
    
    
    def processString(self, message):
        if message:
            if message[0] == '/':
                if len(message) == 1:
                    return
                if message[1] == '/':
                    self.commandHandler.chat(message[1:])
                else:
                    try:
                        command, _sep, arg = message[1:].partition(' ')
                        try:
                            self.commandHandler.execute([command, arg])
                        except Exception as e:
                            self.log(e)
                    except InvalidCommandException as e:
                        self.client.log(", ".join(e.args))
            else:
                self.commandHandler.chat(message)
    
    def startTyping(self, startText=""):
        self.typing = True
        if startText and not self.string:
            self.string = startText
            self.cursor = len(self.string)
            
        self.showString()
    
    def showString(self):
        self.client.display.setInputString(self.string, self.cursor if self.typing else -1)
    
    def addKey(self, key):
        if curses.ascii.isprint(key):
            self.string = self.string[:self.cursor] + chr(key) + self.string[self.cursor:]
            self.cursor += 1
        elif key == curses.KEY_BACKSPACE or key == curses.ascii.BS or key == curses.ascii.DEL:
            self.string = self.string[:self.cursor-1] + self.string[self.cursor:]
            self.cursor = max(self.cursor - 1, 0)
        elif key == curses.KEY_RIGHT:
            self.cursor = min(self.cursor + 1, len(self.string))
        elif key == curses.KEY_LEFT:
            self.cursor = max(self.cursor - 1, 0)
        elif key == curses.KEY_DC:
            self.string = self.string[:self.cursor] + self.string[self.cursor+1:]
        elif key == curses.KEY_HOME:
            self.cursor = 0
        elif key == curses.KEY_END:
            self.cursor = len(self.string)
        
        elif key == curses.ascii.ESC or key == curses.KEY_DL:
            # throw away entered string and go back to game
            self.typing = False
            self.string = ""
            self.cursor = 0
        elif key == curses.ascii.LF or key == curses.ascii.CR:
            # process entered string and reset it
            message = self.string
            self.string = ""
            self.cursor = 0
            self.typing = False
            self.processString(message)
        elif key == curses.ascii.TAB:
            # return to game but keep entered string
            self.typing = False
        
        self.showString()
    
    
    
    
