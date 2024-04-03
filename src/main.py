# Importation
import pygame
from loader import *
from logger import *

# Initialization logger
logs_init(param_get("log_active"))

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(param_get("screen_size"))
clock = pygame.time.Clock()
running = True

param_get("test")

while running:
    # Poll for events
    # Pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # Flip() the display to put your work on screen
    pygame.display.flip()

    fps = param_get("fps")
    clock.tick(fps)  # FPS limit (here to 60 fps)


pygame.quit()