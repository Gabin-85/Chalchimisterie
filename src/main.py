import pygame, console, file, entity, map
from args import path

# Init the logging
console.add_logfile(path.bin+"logs", True)

# Creating the window
screen = pygame.display.set_mode([720, 480])
pygame.display.set_caption("Chalchimisterie")
pygame_clock = pygame.time.Clock()

# Create background
map.create_background(["background1"])
map.load_background(["background1"])
main_background = map.backgrounds["background1"]

# Create entity
entity.new("arbre")
entity.set_flag(0, "draw")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(main_background, [0, 0])

    entity.draw_group(screen)

    pygame.display.flip()

    pygame_clock.tick(60)

# Close all ressources
map.unload_background(map.loaded_background.copy())
map.unload_tilemap(map.loaded_tilemaps.copy())
file.close(file.files.copy())
pygame.quit()