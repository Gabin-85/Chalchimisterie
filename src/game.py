import pygame
import pytmx
import pyscroll
from random import randint
from utils.storageHandler import *
from utils.consoleHandler import *

class Game:

    def __init__(self):

        # Setting live variables
        self.zoom = param_get("zoom")
        self.fps = param_get("fps")

        # Creating game window
        self.screen = pygame.display.set_mode(param_get("screen_size"))
        pygame.display.set_caption(param_get("window_name"))
        self.clock = pygame.time.Clock()

        # Load map (tmx file)
        tmx_data = pytmx.util_pygame.load_pygame("textures/map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = self.zoom

        # Draw calc group
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)


    def run(self):

        running = True

        while running:

            # Pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw everything
            self.group.draw(self.screen)
            pygame.display.flip()

            # FPS limit (update every frame)
            self.clock.tick(self.fps)


    def quit(self):

        # Save and quit
        param_reset("shortcuts", shortcuts)
        param_set(["zoom", "fps"], [self.zoom, self.fps])

        pygame.quit()