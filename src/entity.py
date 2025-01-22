import pygame, console, file
from args import ext, path

group:pygame.sprite.Group = pygame.sprite.Group()
sprites:list[pygame.sprite.Sprite] = []
entities:list = []

def new(name) -> None:
    template = {
        "name":name,
        "flags":set()
    }
    entities.append(template)

def set_flag(id, flag) -> None:
    if flag in entities[id]["flags"]:
        return
    match flag:
        case "draw":
            entities[id]["sprites"] = [len(sprites)]
            sprite = pygame.sprite.Sprite()
            sprite.image, = file.ask([path.bin+"empty"+ext.image])
            sprite.rect = sprite.image.get_rect()
            sprite.add(group)
            sprites.append(sprite)
        case _:
            pass
                
    

def draw_group(surface) -> None:
    group.draw(surface)