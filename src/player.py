from utils.sceneHandler import scene
import pygame

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
        self.friction = 0.8
        # After this you can add varaibles for the player like inventory and others stuffs :

    def get_image(self, x, y):
        image = pygame.Surface([32, 64])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 64))
        return image
        
    def phyiscs(self, dt):
        self.feet = pygame.Rect(self.rect.centerx-15, self.rect.centery-5, 19, 16)
        feetx = self.feet
        feety = self.feet

        self.velocity = self.velocity * self.friction
        self.velocity += self.acceleration

        feetx.x += self.velocity.x
        feety.y += self.velocity.y

        # TODO: Modify the player move part so we can separate x and y
        for wall in scene.get_walls():
            if feetx.colliderect(wall["rect"]) == True:
                match wall["collision_type"]:
                    case "bouncy":
                        pass
                    case "sticky":
                        pass
                    case "solid":
                        self.velocity.x = 0
            if feety.colliderect(wall["rect"]) == True:
                match wall["collision_type"]:
                    case "bouncy":
                        pass
                    case "sticky":
                        pass
                    case "solid":
                        self.velocity.y = 0

        self.rect.center += (self.velocity + (self.velocity/2))*dt
        self.feet = pygame.Rect(self.rect.centerx-15, self.rect.centery-5, 19, 16)
        self.acceleration = pygame.Vector2(0, 0)

    def move(self):
        # TODO: Modifiy this to make set the player acceleration, merge it to the velocity, check here the collisions and update afterwards the position.
        pressed = pygame.key.get_pressed()

        self.acceleration = pygame.Vector2(0, 0)
        if pressed[pygame.K_LEFT]:
            self.acceleration.x -= self.force
        if pressed[pygame.K_RIGHT]:
            self.acceleration.x += self.force
        if pressed[pygame.K_UP]:
            self.acceleration.y -= self.force
        elif pressed[pygame.K_DOWN]:
            self.acceleration.y += self.force

    def update(self, dt):
        self.move()
        self.phyiscs(dt)