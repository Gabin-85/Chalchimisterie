# Importation
import pygame
from random import randint
from utils.storageHandler import *
from utils.consoleHandler import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(param_get("screen_size"))
clock = pygame.time.Clock()
running = True

while running:
    # Poll for events
    # Pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE

    # Flip() the display to put your work on screen
    pygame.display.flip()

    fps = param_get("fps")
    clock.tick(fps)  # FPS limit

# Save and quit
param_reset("shortcuts", shortcuts)

pygame.quit()