# Importation
import pygame
from game import Game

if __name__ == "__main__":
    # Initialisation of pygame
    pygame.init()

    # Call for game
    game = Game()

    # While running
    game.run()

    # Quit
    game.quit()