import pygame, console, file, entity, map, event, cProfile

# Init the logging
console.add_logfile(file.path.bin+"logs")

# Creating the window
screen = pygame.display.set_mode([720, 480])
event.set_allowed_event(event.allowed)
pygame.display.set_caption("Chalchimisterie")
pygame_clock = pygame.time.Clock()

# Create background
map.create_background("background1")
map.load_background("background1")
main_background = map.backgrounds["background1"]

# Create entity
entity_id = entity.new_entity("entity")
sprite_id = entity.new_sprite("sprite")
group_id = entity.new_group("group")
entity.set_entity_sprite(entity_id, sprite_id)
entity.set_sprite_image(sprite_id, file.ask(file.path.bin+"empty"+file.ext.image))
entity.set_sprite_group(sprite_id, group_id)

while event.state.running:
    event.update()
    if 27 in event.state.key:
        event.quit_game()
    if 32 in event.state.key_press:
        console.info("Jump")

    screen.blit(main_background, [0, 0])

    entity.draw_group(screen, group_id)

    pygame.display.flip()

    pygame_clock.tick(60)

# Close all ressources
map.unload_all_backgrounds()
map.unload_all_tilemaps()
console.dump_all_logfiles()
file.files.clear()
pygame.quit()