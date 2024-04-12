# This game file is not the game logic, it's the handling of the game and the rendering part.
import pygame, pytmx, pyscroll
from utils.storageHandler import *
from utils.consoleHandler import *
from utils.mapHandler import *

from player import *

class Game:

    def __init__(self):
        # Get variables
        self.screen_size, self.window_name, self.zoom = param_getlist(["screen_size","window_name", "map_zoom"])

        # Renderer part
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.window_name)

        tmx_data = pytmx.util_pygame.load_pygame("assets/maps/test.tmx")
        map_data = pyscroll.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = get_map_zoom(self.zoom, self.screen_size[0], self.screen_size[1])

        self.walls=[]

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        Player.position = tmx_data.get_object_by_name("player").x,tmx_data.get_object_by_name("player").y
        self.player = Player()

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

    def run(self):
        """
        This is runned every frame. It is the frame.
        """

        # Update the player
        self.player.player_move()

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back()

        self.player.update()

        # Recenter and draw
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        """
        This is empty for the moment.
        """
        ...