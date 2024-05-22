# This game file is not the game logic, it's the handling of the game and the rendering part.
import pygame, pyscroll
from utils.consoleSystem import info
from utils.resourcesHandler import storage, save
from utils.entityHandler import entity_handler
from utils.loadHandler import load
from utils.mathToolbox import Vector2D

class Game:

    def __init__(self):
        """
        This is the game init function. It's called at the beginning of the game.
        """
        # Initialisation
        self.window_name, self.fps_target = storage.get(["window_name","fps"])
        self.screen = pygame.display.set_mode(storage.get("screen_size"))
        pygame.display.set_caption(self.window_name)

        # Load the correct map
        self.selected_scene, self.selected_map = "scene1", "testa"
        if entity_handler.entities is not None:
            for entity in entity_handler.entities:
                if entity["name"] == "player":
                    self.selected_scene, self.selected_map = entity["scene_name"], entity["map_name"]
        self.update_map(self.selected_map, self.selected_scene)

        info("Game launched.")

    def quit(self):
        # We save the game
        for entity in entity_handler.entities:
            entity.unload()
        save.set("entities", entity_handler.entities)
        info("Game closed.")
    
    def update_map(self, map_name=None, scene_name=None):
        if scene_name is None:
            scene_name = self.selected_scene
        if map_name is None:
            map_name = self.selected_map

        load.change_map(map_name, scene_name)
        load.scene_cleanup()

    def physics(self, dt):
        """
        Update the player position and make a draw call.
        """

        # Check if a key is pressed and set the player acceleration
        pressed = pygame.key.get_pressed()
        
        for entity in entity_handler.shown_entities:

            if entity.pattern == "player":
                entity.acceleration = Vector2D(0, 0)
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
                entity.acceleration.inormalize()

            entity.change_frame()

            entity.update(dt)
            if entity.name == "player":
                if entity.map_name != load.selected_map or entity.scene_name != load.selected_scene:
                    self.update_map(entity.map_name, entity.scene_name)
                self.group.center(entity.rect.center)

    def render(self):
        """
        Render the game.
        """
        # Check if entity need to be updated
        if entity_handler.need_update:
            entity_handler.shown_entities = [entity for entity in entity_handler.entities if entity.map_name == load.selected_map and entity.scene_name == load.selected_scene]
            self.group = pyscroll.PyscrollGroup(map_layer=load.get_map_layer(load.selected_map, load.selected_scene), default_layer=4)
            for entity in entity_handler.shown_entities:
                self.group.add(entity)
            self.need_update = False

        # Draw the screen
        self.group.draw(self.screen)
        pygame.display.flip()