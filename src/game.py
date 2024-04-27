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

        # Need to update player position at launch.
        # TODO: Make it configurable with saved files.
        Player.position = (400, 400)
        self.player = Player()

        self.update_render("scene1", "test")

    def update_render(self, scene_name=None, map_name=None):
        # Get all scenes and choose a scene.
        # TODO: Add more scenes and make it save configurable.
        if scene_name is None:
            scene_name = scene.selected_scene
        if map_name is None:
            map_name = scene.selected_map
        scene.change_scene(scene_name)
        scene.selected_map = map_name

        self.group = pyscroll.PyscrollGroup(map_layer=scene.map_layer(map_name), default_layer=4)
        self.group.add(self.player)

    def run(self):
        """
        Update the player position and make a draw call.
        """

        # Update the player movement.
        self.player.move()

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