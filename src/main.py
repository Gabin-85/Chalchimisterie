# This main file launch all files, dependencies and loop the bases functions.
import pygame
from utils.consoleSystem import console
from utils.resourcesHandler import storage, save
# Manage saves
save.handler_default = "save1"
if save.handler_default not in save.paths:
    save.create_file(save.handler_default, "json")
    save.write_file(save.handler_default, {"entities": [], "shown_entities": [], "loaded_scenes": []})
from utils.entityHandler import entity_handler
from utils.loadHandler import load
from game import Game

if __name__ == "__main__":
    # Initialisation
    pygame.init()
    game = Game()

    # This is the code run
    fps_clock = pygame.time.Clock()
    running = True
    while running:
    

        # Quit event registration
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        # Game loop
        game.render()
        game.physics(50 / fps_clock.get_fps() if fps_clock.get_fps() != 0 else 0.8)

        fps_clock.tick(game.fps_target)

    # Quit (The inverse order of initialization)
    game.quit()
    load.quit()
    entity_handler.quit()
    save.quit()
    storage.quit()
    console.quit()
    pygame.quit()