import pygame


entities:list[dict] = []
sprites:list[pygame.sprite.Sprite] = []
groups:list[pygame.sprite.Group] = []


def new_entity(name:str) -> int:
    entities.append({"name":name, "flags":set()})
    return len(entities)-1

def new_sprite(name:str) -> int:
    sprites.append(pygame.sprite.Sprite())
    sprites[-1].name = name
    return len(sprites)-1

def new_group(name:str) -> int:
    groups.append(pygame.sprite.Group())
    groups[-1].name = name
    return len(groups)-1


def get_entity_by_name(name:str) -> list[int]:
    return [entities.index(entity) for entity in entities if entity["name"] == name]

def get_sprite_by_name(name:str) -> list[int]:
    return [sprites.index(sprite) for sprite in sprites if sprite["name"] == name]

def get_group_by_name(name:str) -> list[int]:
    return [groups.index(group) for group in groups if group["name"] == name]


def set_entity_sprite(entity_id:int, sprite_id:int) -> int:
    if "sprites" not in entities[entity_id]["flags"]:
        entities[entity_id]["sprites_id"] = []
        entities[entity_id]["flags"].add("sprites")
    entities[entity_id]["sprites_id"].append(sprite_id)

def set_sprite_image(sprite_id:int, image:pygame.surface.Surface) -> None:
    if "sprites" not in entities[sprite_id]["flags"]:
        print(f"The entity '{sprite_id}' don't have sprites")
    sprites[sprite_id].image = image
    sprites[sprite_id].rect = image.get_rect()

def set_sprite_group(sprite_id:int, group_id:int) -> None:
    groups[group_id].add(sprites[sprite_id])


def get_entity_sprites(entity_id:int) -> list[int]:
    if "sprites" not in entities[entity_id]["flags"]:
        print(f"The entity '{entity_id}' don't have sprites")
    return entities[entity_id]["sprites_id"]

def get_sprite_groups(sprite_id:int) -> list[int]:
    return [groups.index(group) for group in sprites[sprite_id].groups()]
                

def draw_group(surface:pygame.surface.Surface, group_id:int) -> None:
    groups[group_id].draw(surface)