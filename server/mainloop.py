

import gameserver
import room
import argparse
#import threading
import time
#import os
#import signal
import sys
import world
import view
import worldgen


class Game:
    
    def __init__(self):
        
        self.server = gameserver.GameServer(self)
        
        self.world = world.World(worldgen.generateWorld())
        
        self.view = view.View(self.world)
    
        
    def start(self, address):
        
        self.server.start(address)
        
        self.game_loop()
    
    
    def game_loop(self):
        
        keepRunning = True
        while keepRunning:
            
            self.update()
            self.sendState()
            time.sleep(0.05)
    
    def update(self):
        
        messages = self.server.readMessages()
        
        for msg in messages:
            t = msg[0]
            name = msg[1]
            if t == "join":
                if not self.world.hasPlayer(name):
                    self.world.createPlayer(name)
                self.world.playerJoin(name)
            elif t == "leave":
                self.world.removePlayer(name)
            elif t == "input":
                self.world.controlPlayer(name, msg[2])
            
        
        self.world.update()
    
    def sendState(self):
        
        self.server.sendState(self.view)
        



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--socket', help='The socket file to listen to. Use this if the default socket exists already.\nWARNING: if the given file exists it will be overwritten.\nDefaults to /tmp/tron_socket', default="/tmp/tron_socket")
    args = parser.parse_args()
    
    Game().start(args.socket)
