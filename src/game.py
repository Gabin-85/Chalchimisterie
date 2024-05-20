# This game file is not the game logic, it's the handling of the game and the rendering part.
import pygame, pyscroll
from utils.resourcesHandler import storage
from utils.loadHandler import load
from utils.saveHandler import saver

class Game:

    def __init__(self):
        """
        This is the game init function. It's called at the beginning of the game.
        """
        self.fps_clock = pygame.time.Clock()
        self.window_name = storage.get("window_name")
        self.screen = pygame.display.set_mode(storage.get("screen_size"))
        pygame.display.set_caption(self.window_name)

        # Load the correct map
        self.selected_scene, self.selected_map = "scene1", "testa"
        if saver.save["entities"] is not None:
            for entity in saver.save["entities"]:
                if entity["name"] == "player":
                    self.selected_scene, self.selected_map = entity["scene_name"], entity["map_name"]
        self.update_map(self.selected_map, self.selected_scene)

    def quit(self):
        # We save the game
        for entity in saver.get_entities():
            print(entity.name)
            entity.unload()
    
    def update_map(self, map_name=None, scene_name=None):
        if scene_name is None:
            scene_name = self.selected_scene
        if map_name is None:
            map_name = self.selected_map

        load.change_map(map_name, scene_name)
        load.scene_cleanup()

        self.group = pyscroll.PyscrollGroup(map_layer=load.get_map_layer(map_name, scene_name), default_layer=4)
        for entity in saver.get_entities():
            self.group.add(entity)

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

        # Check if a key is pressed and set the player acceleration
        pressed = pygame.key.get_pressed()
        
        for entity in saver.get_entities():

            if entity.name == "player":
                entity.acceleration = pygame.Vector2(0, 0)
                if pressed[pygame.K_LEFT]:
                    entity.acceleration.x -= 1
                    entity.change_animation("left")
                if pressed[pygame.K_RIGHT]:
                    entity.acceleration.x += 1
                    entity.change_animation("right")
                if pressed[pygame.K_UP]:
                    entity.acceleration.y -= 1
                    entity.change_animation("up")
                if pressed[pygame.K_DOWN]:
                    entity.acceleration.y += 1
                    entity.change_animation("down")

            entity.change_frame()

            entity.update(dt)
            if entity.name == "player":
                if entity.map_name != load.selected_map or entity.scene_name != load.selected_scene:
                    self.update_map(entity.map_name, entity.scene_name)
                self.group.center(entity.rect.center)
        self.group.draw(self.screen)
        pygame.display.flip()