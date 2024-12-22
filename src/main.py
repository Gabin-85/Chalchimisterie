from utils.console import logger
from utils.file import file
import pygame
from map import background, tilemap

# Init the logging
logger.select("logs")

#Creating the window
screen = pygame.display.set_mode([720, 480])
pygame.display.set_caption("Chalchimisterie")
pygame_clock = pygame.time.Clock()

background.create("background1")
main_background = background.backgrounds["background1"]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(main_background, [0, 0])

    pygame.display.flip()

    pygame_clock.tick(60)

background.unload(*background.loaded_background)
tilemap.unload(*tilemap.loaded_tilemaps)
file.close(*file.files)

pygame.quit()