# This main file launch all files, dependencies and loop the bases functions.
import pygame
from utils.storageHandler import storageHandler
from utils.consoleHandler import consoleHandler
from game import Game
from game_logic import Game_logic

if __name__ == "__main__":
    # Initialisation
    pygame.init()
    storage = storageHandler()
    console = consoleHandler()
    game = Game()
    game_logic = Game_logic()

    # This is the code run
    running = True
    while running:

        # Quit event registration
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        # Game logic part
        game_logic.run()

        # Game showing stuff
        game.run()


    # Quit (The inverse order of initialization)
    game_logic.quit()
    game.quit()
    console.quit()
    storage.quit()
    pygame.quit()