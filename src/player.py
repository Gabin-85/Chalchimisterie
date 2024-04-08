import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("assets/sprites/player/player.png")
        self.image = self.get_image(6, 14)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.position = [x, y]

    # Player mouvement
    def update(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.position[1] -= 1
        elif pressed[pygame.K_DOWN]:
            self.position[1] += 1
        elif pressed[pygame.K_LEFT]:
            self.position[0] -= 1
        elif pressed[pygame.K_RIGHT]:
            self.position[0] += 1

        self.rect.topleft = self.position
        
    def get_image(self, x, y):
        image = pygame.Surface([32, 64])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 64))
        return image