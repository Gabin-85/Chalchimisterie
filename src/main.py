# Importation
import pygame

# Class importation
from utils.storageHandler import storageHandler
from utils.consoleHandler import consoleHandler
from renderer import Render
from game import Game

if __name__ == "__main__":
    # Initialisation
    pygame.init()
    storage = storageHandler()
    console = consoleHandler()
    render = Render()
    game = Game()

    # This is the code run
    running = True
    while running:

        # Quit event registration
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        # Here is the game logic
        game.run()

        # RENDERING
        # The setup part is here to change the payload of the renderer
        render.run()


    # Quit (The inverse order of initialization)
    game.quit()
    render.quit()
    console.quit()
    storage.quit()
    pygame.quit()