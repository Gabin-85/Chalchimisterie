from utils.console import logger
from utils.file import file
from map import background, tilemap
import pygame

# Init the logging
logger.init("logs")

#Creating the window
screen = pygame.display.set_mode([720, 480])
pygame.display.set_caption("Chalchimisterie")
pygame_clock = pygame.time.Clock()

background.create("background1")
background.load("background1")
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