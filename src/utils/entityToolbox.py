from utils.sceneHandler import scene
from animation import EntityAnimation
import pygame
import math

class EntityAnimation():
    pass

class BaseEntity(pygame.sprite.Sprite):
    
    #TODO: Set a pattern to entities.

    def __init__(self, name) -> None:
        super().__init__()

        # Position
        self.scene_name = None
        self.map_name = None
        self.position = pygame.Vector2(0, 0)

    def quit(self):
        # Save here the positions
        pass

class StandardEntity(BaseEntity):
    
    def __init__(self, name) -> None:
        super().__init__(name)
        # Hitbox
        self.hitbox = pygame.Rect(0, 0, 0, 0)

    def quit(self):
        # Save here nothing
        pass


class DynamicEntity(StandardEntity):
    
    def __init__(self, name) -> None:
        super().__init__(name)
        # Hitbox
        self.hurtbox = pygame.Rect(0, 0, 0, 0)

        # Physics
        self.velocity = pygame.Vector2(0, 0)
        self.mass = 1.0
        self.force = 1.0
        self.friction = 1.0

        # Animation
        self.animation = EntityAnimation(name, (0, 0), 0)

    def quit(self):
        # Save here the animation
        pass

    def update(self, dt):
        self.velocity -= self.velocity * self.friction / self.mass - self.acceleration

        marging = pygame.Vector2(0, 0)
        if self.velocity.x > 0:
            marging.x = math.ceil(self.velocity.x)
        else:
            marging.x = math.floor(self.velocity.x)
        if self.velocity.y > 0:
            marging.y = math.ceil(self.velocity.y)
        else:
            marging.y = math.floor(self.velocity.y)
        feetx = pygame.Rect(self.hitbox.x + marging.x, self.hitbox.y, self.hitbox.width, self.hitbox.height)
        feety = pygame.Rect(self.hitbox.x, self.hitbox.y + marging.y, self.hitbox.width, self.hitbox.height)

        # TODO: Modify the player move part so we can separate x and y
        for wall in scene.get_walls():
            if feetx.colliderect(wall["rect"]) == True:
                match wall["collision_type"]:
                    case "bouncy":
                        self.velocity.x *= -1
                    case "sticky":
                        self.velocity.x = 0
                        self.velocity.y = 0
                    case "solid":
                        self.velocity.x = 0
            if feety.colliderect(wall["rect"]) == True:
                match wall["collision_type"]:
                    case "bouncy":
                        self.velocity.y *= -1
                    case "sticky":
                        self.velocity.x = 0
                        self.velocity.y = 0
                    case "solid":
                        self.velocity.y = 0

        self.position += self.velocity*dt
        self.hitbox.center = self.position
        self.rect.center = (self.hitbox.x+10, self.hitbox.y-6)

        # Teleport the player if he collide with a portal
        for portal in scene.get_portals():
            if self.hitbox.colliderect(scene.get_portals()[portal]["rect"]) == True:
                self.position.x, self.position.y = scene.get_portal_exit(scene.get_portals()[portal]).x, scene.get_portal_exit(scene.get_portals()[portal]).y
                self.map_name, self.scene_name = scene.get_portals()[portal]["targeted_map_name"], scene.get_portals()[portal]["targeted_scene_name"]