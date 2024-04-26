# This game file is not the game logic, it's the handling of the game and the rendering part.
import pygame, pytmx, pyscroll
from utils.storageHandler import param_get
from utils.sceneHandler import scene

from player import *

class Game:

    def __init__(self):
        """
        This is the game init function. It's called at the beginning of the game.
        """

        # Get variables
        self.window_name = param_get("window_name")

        # Renderer part
        self.screen = pygame.display.set_mode(param_get("screen_size"))
        pygame.display.set_caption(self.window_name)

        # Get all scenes and choose a scene
        # TODO: Add more scenes and make it save configurable
        scene.change_scene("scene1")
        scene.map_name = "test"

        # Set map layer and player
        map_layer = pyscroll.orthographic.BufferedRenderer(scene.map_data(), self.screen.get_size())
        map_layer.zoom = scene.get_map_zoom()

        Player.position = scene.player().x, scene.player().y
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
            if sprite.feet.collidelist(scene.walls()["sticky"]) > -1:
                pass
            elif sprite.feet.collidelist(scene.walls()["bouncy"]) > -1:
                pass
            elif sprite.feet.collidelist(scene.walls()["solid"]) > -1:
                self.player.move_back()
            elif sprite.feet.collidelist(scene.portals()) > -1:
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