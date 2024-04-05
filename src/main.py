# Importation
import pygame
from loader import *
from logger import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(param_get("screen_size"))
clock = pygame.time.Clock()
running = True

# This is the loader test (the shortcuts part and half the functions)
if file_create("test.json", None, {"test": "test"}, "test2") == True: DEBUG("Created test passed")
if file_rename("test2", "test3", "test") == True: DEBUG("Renamed test passed")
if param_set(["one", "two"], ["tree", "four"], "test") == True: DEBUG("Setlist test passed")
one, two = param_getlist(["one", "two"])
if one == "tree" and two == "four": DEBUG("Getlist test passed")
if param_del(["one", "two"], "test") == True: DEBUG("Dellist test passed")
if param_reset("test", {"pass test": "test"}) == True: DEBUG("Reset   test passed")
if file_delete("test") == True: DEBUG("Deleted test passed")
if file_create("test", ".txt", "test") == True: DEBUG("Created test passed")
if file_delete("test") == True: DEBUG("Deleted test passed")
# End of loader test

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

# Save and quit
param_reset("shortcuts", shortcuts)

pygame.quit()