# Importation
import pygame
from random import randint
from utils.storageHandler import *
from utils.consoleHandler import *
from tile import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(param_get("screen_size"))
clock = pygame.time.Clock()
running = True

scene = param_get("scene_name")
if scene == "scene2" or scene == None:
    tiles = param_get("scene1")
    image = tile_map_draw(param_get("empty_grass"), tiles[0], tiles[1], tiles[2])
    scene = "scene1"
elif scene == "scene1":
    tiles = param_get("scene2")
    image = tile_map_draw(param_get("empty_grass"), tiles[0], tiles[1], tiles[2])
    scene = "scene2"

while running:
    # Poll for events
    # Pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if scene == "scene2" or scene == None:
                tiles = param_get("scene1")
                image = tile_map_draw(param_get("empty_grass"), tiles[0], tiles[1], tiles[2])
                scene = "scene1"
            elif scene == "scene1":
                tiles = param_get("scene2")
                image = tile_map_draw(param_get("empty_grass"), tiles[0], tiles[1], tiles[2])
                scene = "scene2"

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    for i in range(1200):
        screen.blit(image[0][i], (image[1][i], image[2][i]))

    # Flip() the display to put your work on screen
    pygame.display.flip()

    fps = param_get("fps")
    clock.tick(fps)  # FPS limit

# Save and quit
param_reset("shortcuts", shortcuts)
param_set("scene_name", scene, "save")

pygame.quit()