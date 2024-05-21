from utils.entityToolbox import Entity
import pygame

class mush():
    def __init__(self):
        self.mush = Entity()
        self.mush.load(0)
        
    def quit(self):
        self.mush.unload()

    def update(self, dt):
        self.move()
        self.mush.update(dt)
