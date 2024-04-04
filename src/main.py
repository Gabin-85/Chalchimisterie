# Importation
import pygame
from loader import *
from logger import *

# Initialization
logs_init(param_get("log_active"))

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(param_get("screen_size"))
clock = pygame.time.Clock()
running = True

# This is the loader test (the shortcuts part and half the functions)
if file_create("test.json", None, None, "test2") == True: DEBUG("File created")
if file_rename("test2", "test3", "test") == True: DEBUG("File renamed")
if param_setlist(["one", "two"], ["tree", "four"], ["test", "test"]) == True: DEBUG("Setlist test passed")
one, two = param_getlist(["one", "two"])
if one == "tree" and two == "four": DEBUG("Getlist test passed")
if param_dellist(["one", "two"], ["test", "test"]) == True: DEBUG("Dellist test passed")
if param_reset("test", {"pass test": "test"}) == True: DEBUG("Reset test passed")
if file_delete("test") == True: DEBUG("File deleted")
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