from utils.entityToolbox import Entity
import pygame

class Player():

    def __init__(self):
        self.player = Entity()
        self.player.load(0)
        
    def quit(self):
        self.player.unload()

    def update(self, dt):
        self.move()
        self.player.update(dt)

    def move(self):
        # Check if a key is pressed and set the player acceleration
        pressed = pygame.key.get_pressed()

        self.player.acceleration = pygame.Vector2(0, 0)
        if pressed[pygame.K_LEFT]:
            self.player.acceleration.x -= 1
            self.player.change_animation("left")
        if pressed[pygame.K_RIGHT]:
            self.player.acceleration.x += 1
            self.player.change_animation("right")
        if pressed[pygame.K_UP]:
            self.player.acceleration.y -= 1
            self.player.change_animation("up")
        if pressed[pygame.K_DOWN]:
            self.player.acceleration.y += 1
            self.player.change_animation("down")

        self.player.change_frame()