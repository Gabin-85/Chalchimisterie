# Rendering section
import pygame
import pytmx
import pyscroll
# Handlers section
from utils.storageHandler import *
from utils.consoleHandler import *

class Render:

    def __init__(self):

        # Get parameters
        self.zoom, self.fps = param_getlist(["zoom", "fps"], "default")

        # Creating game window
        self.screen = pygame.display.set_mode(param_get("screen_size"))
        pygame.display.set_caption(param_get("window_name"))
        self.clock = pygame.time.Clock()

    def setup(self):
         # Load map (tmx file)
        tmx_data = pytmx.util_pygame.load_pygame("textures/map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = self.zoom

        # Draw calc group
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    def run(self):

            # Draw everything
            self.group.draw(self.screen)
            pygame.display.flip()

            # FPS limit (update every frame)
            self.clock.tick(self.fps)

    def quit(self):
        param_set(["zoom", "fps"], [self.zoom, self.fps], "default")