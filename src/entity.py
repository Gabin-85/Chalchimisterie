import pygame, file

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
            sprite.image, = file.ask([file.path.bin+"empty"+file.ext.image])
            sprite.rect = sprite.image.get_rect()
            sprite.add(group)
            sprites.append(sprite)
        case _:
            pass
                
    

def draw_group(surface) -> None:
    group.draw(surface)