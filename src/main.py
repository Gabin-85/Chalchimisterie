# This main file launch all files, dependencies and loop the bases functions.
import pygame
from utils.consoleSystem import console
from utils.resourcesHandler import storage, save
from utils.loadHandler import load
from utils.saveHandler import saver
from game import Game

if __name__ == "__main__":
    # Initialisation
    pygame.init()
    saver.setup("save1")
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
        game.physics(50 / fps_clock.get_fps() if fps_clock.get_fps() != 0 else 0.8)
        game.render()

        fps_clock.tick(game.fps_target)

    # Quit (The inverse order of initialization)
    game.quit()
    saver.quit()
    load.quit()
    save.quit()
    storage.quit()
    console.quit()
    pygame.quit()