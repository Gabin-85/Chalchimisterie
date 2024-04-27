import pygame
import math

DIAGONALY = math.sqrt(2)/2

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.sprite_sheet = pygame.image.load("assets/sprites/player/player.png")
        self.image = self.get_image(6, 14)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.last_position = [None, None]
        self.feet = pygame.Rect(0, 0, 0, 0)
        self.glide = 0.5
        self.allow_move = True
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        
        # After this you can add varaibles for the player like inventory and others stuffs :

    def get_image(self, x, y):

        image = pygame.Surface([32, 64])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 64))
        return image

    def move(self):
        # TODO: Modifiy this to make set the player acceleration, merge it to the velocity, check here the collisions and update afterwards the position.
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
            self.acceleration = [0.8, 0.8]
        else:
            self.acceleration = [0.5, 0.5]

        if pressed[pygame.K_UP] and not pressed[pygame.K_DOWN]:
            if pressed[pygame.K_LEFT] and not pressed[pygame.K_RIGHT]:
                self.acceleration = [-self.acceleration[0]*DIAGONALY, -self.acceleration[1]*DIAGONALY]
            elif pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
                self.acceleration = [self.acceleration[0]*DIAGONALY, -self.acceleration[1]*DIAGONALY]
            else:
                self.acceleration = [0, -self.acceleration[1]]
        elif pressed[pygame.K_DOWN] and not pressed[pygame.K_UP]:
            if pressed[pygame.K_LEFT] and not pressed[pygame.K_RIGHT]:
                self.acceleration = [-self.acceleration[0]*DIAGONALY, self.acceleration[1]*DIAGONALY]
            elif pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
                self.acceleration = [self.acceleration[0]*DIAGONALY, self.acceleration[1]*DIAGONALY]
            else:
                self.acceleration = [0, self.acceleration[1]]
        else:
            if pressed[pygame.K_LEFT] and not pressed[pygame.K_RIGHT]:
                self.acceleration = [-self.acceleration[0], 0]
            elif pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
                self.acceleration = [self.acceleration[0], 0]
            else:
                self.acceleration = [0, 0]
        if pressed[pygame.K_SPACE]:
            self.acceleration = self.acceleration[0]*500, self.acceleration[1]*500
            if self.allow_move: 
                self.velocity = self.velocity[0]*self.glide + self.acceleration[0]*(-self.glide+1), self.velocity[1]*self.glide + self.acceleration[1]*(-self.glide+1)
            self.allow_move = False

        if self.allow_move:
            self.velocity = self.velocity[0]*self.glide + self.acceleration[0]*(-self.glide+1), self.velocity[1]*self.glide + self.acceleration[1]*(-self.glide+1)
        else:
            self.velocity = self.velocity[0]*self.glide, self.velocity[1]*self.glide
            if round(self.velocity[0], 1) == 0 and round(self.velocity[1], 1) == 0:
                self.allow_move = True


        self.position = [self.position[0]+self.velocity[0], self.position[1]+self.velocity[1]]
        self.feet = pygame.Rect(self.position[0], 28+self.position[1], 22, 18)

    def update(self):
        """
        For updating your player stats, we have to update the renderer player part.
        All sets bellow are necessary.
        """
        # TODO: Delete this. It has to be in move().
        if self.last_position != self.position:
            self.feet.midbottom = self.rect.midbottom
            self.last_position = self.position
            self.rect.topleft = self.position

    def move_back(self):
        self.position = self.last_position