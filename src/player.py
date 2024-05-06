from utils.sceneHandler import scene
from animation import EntityAnimation
from utils.saveHandler import SaveObject
import pygame
import math

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.player_animation = EntityAnimation("player", (21, 48), 50)
        self.hitbox = pygame.Rect(0, 0, 21, 18)
        self.hurtbox = pygame.Rect(0, 0, 21, 18)
        
        self.position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.mass = 1.0
        self.force = 1.0
        self.friction = 0.2
        
        self.save = SaveObject("player")
        self.position = pygame.Vector2(self.save.get_save("position")[0], self.save.get_save("position")[1])
        self.map_name = self.save.get_save("map_name")
        self.scene_name = self.save.get_save("scene_name")
        # After this you can add variables for the player like inventory and others stuffs :

    def quit(self):
        self.save.set_save("map_name", self.map_name)
        self.save.set_save("scene_name", self.scene_name)
        self.save.set_save("position", (self.position.x, self.position.y))

    def update(self, dt):
        self.move()
        self.phyiscs(dt)

    def move(self):
        # Check if a key is pressed and set the player acceleration
        pressed = pygame.key.get_pressed()

        self.acceleration = pygame.Vector2(0, 0)
        if pressed[pygame.K_LEFT]:
            self.acceleration.x -= 1
            self.player_animation.reset_to("left")
        if pressed[pygame.K_RIGHT]:
            self.acceleration.x += 1
            self.player_animation.reset_to("right")
        if pressed[pygame.K_UP]:
            self.acceleration.y -= 1
            self.player_animation.reset_to("up")
        if pressed[pygame.K_DOWN]:
            self.acceleration.y += 1
            self.player_animation.reset_to("down")
        
        try:
            self.acceleration.scale_to_length(self.force/self.mass)
        except:
            pass

        self.rect = self.player_animation.next()
        self.image = self.player_animation.current_image
            
    def phyiscs(self, dt):
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
