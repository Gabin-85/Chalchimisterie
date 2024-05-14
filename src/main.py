# This main file launch all files, dependencies and loop the bases functions.
import pygame
from utils.consoleSystem import console
from utils.resourcesHandler import storage
from utils.loadHandler import scene
from utils.saveHandler import save
from game import Game

if __name__ == "__main__":
    # Initialisation
    pygame.init()
    save.load_file("save1")
    save.selected_save = "save1"
    game = Game()

    # This is the code run
    running = True
    while running:

        # Quit event registration
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        # Game loop
        game.run()

    # Quit (The inverse order of initialization)
    game.quit()
    scene.quit()
    save.quit()
    storage.quit()
    console.quit()
    pygame.quit()