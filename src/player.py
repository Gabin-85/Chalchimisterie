import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self):
        
        super().__init__()
        self.sprite_sheet = pygame.image.load("assets/sprites/player/player.png")
        self.image = self.get_image(6, 14)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        # After this you can add varaibles for the player like inventory and others stuffs :

    def get_image(self, x, y):

        image = pygame.Surface([32, 64])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 64))
        return image

    def player_move(self):

        pressed = pygame.key.get_pressed()

        speed = 0.5

        if pressed[pygame.K_UP]:
            self.position = [self.position[0], self.position[1]-speed]
        elif pressed[pygame.K_DOWN]:
            self.position = [self.position[0], self.position[1]+speed]
        if pressed[pygame.K_LEFT]:
            self.position = [self.position[0]-speed, self.position[1]]
        elif pressed[pygame.K_RIGHT]:
            self.position = [self.position[0]+speed, self.position[1]]

    def update(self):
        """
        For updating your player stats, we have to update the renderer player part.
        All sets bellow are necessary.
        """

        self.rect.topleft = self.position