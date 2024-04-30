from utils.sceneHandler import scene
from animation import EntityAnimation
import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.player_animation = EntityAnimation("player", (21, 48), 50)
        self.feet = pygame.Rect(0, 0, 21, 16)
        
        self.position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.linear_force = 1.0
        self.diagonal_force = (self.linear_force**2)/2**0.5
        self.friction = 0.8
        # After this you can add variables for the player like inventory and others stuffs :
    
    def update(self, dt):
        self.move()
        self.phyiscs(dt)

    def move(self):
        # Check if a key is pressed and set the player acceleration
        pressed = pygame.key.get_pressed()

        self.acceleration.x, self.acceleration.y = 0, 0
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
        
        if self.acceleration.x != 0 and self.acceleration.y != 0:
            self.acceleration *= self.diagonal_force
        else:
            self.acceleration *= self.linear_force

        self.rect = self.player_animation.next()
        self.image = self.player_animation.current_image
            
    def phyiscs(self, dt):
        self.velocity = self.velocity * self.friction
        self.velocity += self.acceleration

        feetx = pygame.Rect(self.feet.x + self.velocity.x, self.feet.y, self.feet.width, self.feet.height)
        feety = pygame.Rect(self.feet.x, self.feet.y + self.velocity.y, self.feet.width, self.feet.height)

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

        self.position += (self.velocity)*dt
        self.feet.center = self.position
        self.rect.center = (self.feet.x+16, self.feet.y+4)
        self.acceleration = pygame.Vector2(0, 0)