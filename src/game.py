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
        Player.position = (None, None)
        self.player = Player()

        scene.change_scene("scene1")
        self.change_map("test")

    def change_map(self, map_name=None):
        # TODO: Make it save configurable.
        if map_name is None:
            map_name = scene.selected_map
        scene.selected_map = map_name

        if Player.position == (None, None):
            Player.position = (scene.player(map_name).x, scene.player(map_name).y)

        self.group = pyscroll.PyscrollGroup(map_layer=scene.map_layer(map_name), default_layer=4)
        self.group.add(self.player)

    def run(self):
        """
        Update the player position and make a draw call.
        """

        # Update the player movement.
        self.player.move()

        # Teleport the player if he collide with a portal
        for portal in scene.portals():
            if self.player.feet.colliderect(scene.portals()[portal]["rect"]) == True:
                self.player.position = (scene.portal_exit(scene.portals()[portal]).x, scene.portal_exit(scene.portals()[portal]).y)
                self.change_map(scene.portals()[portal]["targeted_map_name"])
        
        # TODO: Modify the player move part so we can separate x and y
        for wall in scene.walls():
            if self.player.feet.colliderect(wall["rect"]) == True:
                match wall["collision_type"]:
                    case "bouncy":
                        pass
                    case "sticky":
                        pass
                    case "solid":
                        self.player.move_back()

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