# Rendering section
import pygame, pytmx, pyscroll
import pytmx.util_pygame

# Handlers section
from utils.storageHandler import *
from utils.consoleHandler import *

from map import *
from player import Player

class Render:

    def __init__(self):
        # Get variables
        screen_size, window_name, zoom = param_getlist(["screen_size","window_name", "map_zoom"])

        # Creating the window
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(window_name)

        # Load the map
        tmx_data = pytmx.util_pygame.load_pygame("assets/maps/test.tmx")
        map_data = pyscroll.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # Getting the real zoom because if you don't do that the map is crap.
        map_layer.zoom = get_map_zoom(zoom, screen_size[0], screen_size[1])

        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # Creating a group
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

    def run(self):

        self.group.update()
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        ...