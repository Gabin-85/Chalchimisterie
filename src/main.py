import pygame, log, file, entity, map, event

# Init the logging
log.set_file(file.path.bin+"logs"+file.ext.log)

# Creating the window
screen = pygame.display.set_mode([720, 480])
event.set_allowed_event(event.allowed)
pygame.display.set_caption("Chalchimisterie")
pygame_clock = pygame.time.Clock()

# Create background
if map.create_background("background1") in ("notexistant", "notvalue"):
    log.error("Can't create background")
if map.load_background("background1") in ("notexistant", "notvalue"):
    log.error("Can't load background")
else:
    main_background = map.backgrounds["background1"]
map.load_tilemap("tilemap1")

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
        log.info("Jump")

    screen.blit(main_background, [0, 0])

    entity.draw_group(screen, group_id)

    pygame.display.flip()

    pygame_clock.tick(60)

# Close all ressources
map.unload_all_backgrounds()
map.unload_all_tilemaps()
log.flush()
file.files.clear()
pygame.quit()