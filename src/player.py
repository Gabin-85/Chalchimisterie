import pygame
import math

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.sprite_sheet = pygame.image.load("assets/sprites/player/player.png")
        self.image = self.get_image(6, 14)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.last_position = [None, None]
        self.feet = pygame.Rect(0, 0, 0, 0)
        # self.glide = 0.5
        # self.allow_move = True
        self.speed = 60
        self.force = 1
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.friction = 0.8
        # After this you can add varaibles for the player like inventory and others stuffs :

    def get_image(self, x, y):
        image = pygame.Surface([32, 64])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 64))
        return image
        
    def phyiscs(self, dt):
        self.velocity.x = self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x
        self.rect.centerx += (self.velocity.x + (self.velocity.x/2))*dt
        self.feet = pygame.Rect(self.rect.centerx, 28+0, 22, 18)
        self.acceleration = pygame.Vector2(0, 0)

    def move(self):
        # TODO: Modifiy this to make set the player acceleration, merge it to the velocity, check here the collisions and update afterwards the position.
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.acceleration.x = -self.force
        elif pressed[pygame.K_RIGHT]:
            self.acceleration.x = self.force
        else:
            self.acceleration.x = 0

    def update(self, dt):
        self.move()
        self.phyiscs(dt)

    def move_back(self):
        self.position = self.last_position