# Rendering section
import pygame
import pytmx
import pyscroll

# Handlers section
from utils.storageHandler import *
from utils.consoleHandler import *

from map import MapManager

class Render:

    def __init__(self):

        # Get parameters
        self.zoom, self.fps = param_getlist(["zoom", "fps"], "default")

        # Creating game window
        self.screen = pygame.display.set_mode(param_get("screen_size"))
        pygame.display.set_caption(param_get("window_name"))
        self.clock = pygame.time.Clock()

        self.map_manager = MapManager(self.screen)

    def update(self):
        # Black magic here (if you don't understand, Don't touch !)
        self.map_manager.get_group()._map_layer.zoom = self.zoom
        #self.map_manager.get_group().update()


    def run(self):

            # Draw everything
            self.map_manager.get_group().draw(self.screen)
            self.map_manager.get_group().center(self.screen.get_rect().center)
            pygame.display.flip()

            # FPS limit (update every frame)
            self.clock.tick(self.fps)

    def quit(self):
        param_set(["zoom", "fps"], [self.zoom, self.fps], "default")