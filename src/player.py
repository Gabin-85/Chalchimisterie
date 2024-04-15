import pygame
from utils.consoleHandler import *
from time import wait

velocity = pygame.Vector2(0, 0)
class Player(pygame.sprite.Sprite):

    def __init__(self):
        
        super().__init__()
        self.sprite_sheet = pygame.image.load("assets/sprites/player/player.png")
        self.image = self.get_image(6, 14)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.last_position = [None, None]
        self.feet = pygame.Rect(0, 0, 0, 0)

        # After this you can add varaibles for the player like inventory and others stuffs :

    def get_image(self, x, y):

        image = pygame.Surface([32, 64])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 64))
        return image

    def player_move(self):
        global velocity;
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
            speed = 0.8
        else:
            speed = 0.5

        if pressed[pygame.K_UP]:
            velocity = [velocity[0], velocity[1]-speed]
        elif pressed[pygame.K_DOWN]:
            velocity = [velocity[0], velocity[1]+speed]
        if pressed[pygame.K_LEFT]:
            velocity = [velocity[0]-speed, velocity[1]]
        elif pressed[pygame.K_RIGHT]:
            velocity = [velocity[0]+speed, velocity[1]]
        # roulade
        if pressed[pygame.K_SPACE]:
            self.position = [velocity[1]*3, velocity[1]*3]
            wait(0.3)
            self.position = [0, 0]
        self.feet = pygame.Rect(self.position[0], 28+self.position[1], 22, 18)

    def update(self):
        """
        For updating your player stats, we have to update the renderer player part.
        All sets bellow are necessary.
        """
        if self.last_position != self.position:
            self.feet.midbottom = self.rect.midbottom
            self.last_position = self.position
            self.rect.topleft = self.position

    def move_back(self):
        self.position = self.last_position