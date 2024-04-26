# This game file is not the game logic, it's the handling of the game and the rendering part.
import pygame, pytmx, pyscroll
from utils.storageHandler import *
from utils.consoleHandler import *
from utils.sceneHandler import *

from player import *

class Game:

    def __init__(self):
        """
        This is the game init function. It's called at the beginning of the game.
        """

        # Get variables
        self.screen_size, self.window_name, self.zoom = param_getlist(["screen_size","window_name", "map_zoom"])

        # Renderer part
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.window_name)

        # Get all scenes and choose a scene
        # TODO: Add more scenes and make it save configurable
        self.scene = sceneHandler("scene1", "test")
        self.scene.change_scene("scene1")

        # Set map layer and player
        map_layer = pyscroll.orthographic.BufferedRenderer(self.scene.map_data(), self.screen.get_size())
        map_layer.zoom = get_map_zoom(self.zoom, self.screen_size[0], self.screen_size[1])

        Player.position = self.scene.player().x, self.scene.player().y
        self.player = Player()

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

    def run(self):
        """
        Update the player position and make a draw call.
        """

        # Update the player movement
        self.player.player_move()

        # TODO: Modify the player move part so we can separate x and y
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.scene.walls()["sticky"]) > -1:
                pass
            elif sprite.feet.collidelist(self.scene.walls()["bouncy"]) > -1:
                pass
            elif sprite.feet.collidelist(self.scene.walls()["solid"]) > -1:
                self.player.move_back()
            elif sprite.feet.collidelist(self.scene.portals()) > -1:
                pass

        # Update the player position
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