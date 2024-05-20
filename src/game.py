# This game file is not the game logic, it's the handling of the game and the rendering part.
import pygame, pyscroll
from utils.resourcesHandler import storage
from utils.loadHandler import scene
from player import Player

class Game:

    def __init__(self):
        """
        This is the game init function. It's called at the beginning of the game.
        """
        self.fps_clock = pygame.time.Clock()

        # Get variables
        self.window_name = storage.get("window_name")

        # Renderer part
        self.screen = pygame.display.set_mode(storage.get("screen_size"))
        pygame.display.set_caption(self.window_name)

        self.player = Player()
        
        self.update_map(self.player.player.map_name, self.player.player.scene_name)

    def quit(self):
        # We save the game
        self.player.quit()
    
    def update_map(self, map_name=None, scene_name=None):
        if scene_name is None:
            scene_name = self.selected_scene
        if map_name is None:
            map_name = self.selected_map

        scene.change_map(map_name, scene_name)
        scene.scene_cleanup()

        self.group = pyscroll.PyscrollGroup(map_layer=scene.get_map_layer(map_name, scene_name), default_layer=4)
        self.group.add(self.player.player)

    def run(self):
        """
        Update the player position and make a draw call.
        """

        # Update the player movement.
        self.fps_clock.tick(60)
        try:
            dt = 50 / self.fps_clock.get_fps()
        except:
            dt = 0
        self.player.update(dt)

        if self.player.player.map_name != scene.selected_map or self.player.player.scene_name != scene.selected_scene:
            self.update_map(self.player.player.map_name, self.player.player.scene_name)

        # Recenter and draw
        self.group.center(self.player.player.rect.center)
        self.group.draw(self.screen)
        pygame.display.flip()