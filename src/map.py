import pygame, file, log
from error import Err

tiles = {}
loaded_tilemaps = set()

def load_tilemap(tilemap_name:str) -> None|Err:
    tilemap_data = file.ask(file.path.tilemap+tilemap_name+file.ext.data)
    tilemap_image = file.ask(file.path.tilemap+tilemap_name+file.ext.image)

    if __debug__ and tilemap_data == "notexixtant":
        tilemap_data.msg += " <- Wrong tilemap_data type"
        return tilemap_data
    
    if __debug__ and tilemap_image == "notexixtant":
        tilemap_image.msg += " <- Wrong tilemap_image type"
        return tilemap_image
    
    if __debug__ and type(tilemap_data) != dict:
        return Err("notvalue", "Can't load tilemap", f"Value : {tilemap_data}")
    
    if __debug__ and type(tilemap_image) != pygame.Surface:
        return Err("notvalue", "Can't load image", f"Value : {tilemap_image}")
    
    for tile in tilemap_data["tiles"]:
        if __debug__ and tile in tiles:
            log.warn(f"The tile {tile!r} as been recall")
        
        x = tilemap_data["tiles"][tile][0]*tilemap_data["tile_size"]
        y = tilemap_data["tiles"][tile][1]*tilemap_data["tile_size"]

        if __debug__ :
            if x+tilemap_data["tile_size"] > tilemap_image.get_width() \
            or y+tilemap_data["tile_size"] > tilemap_image.get_height():
                return Err("overstep", f"Subregion bigger or to far from base image",
                f"{x+tilemap_data["tile_size"]} > {tilemap_image.get_width()}\
                or {y+tilemap_data["tile_size"]} > {tilemap_image.get_height()}")

        tiles[tile] = tilemap_image.subsurface(x, y, tilemap_data["tile_size"], tilemap_data["tile_size"])
    loaded_tilemaps.add(tilemap_name)
    file.close(file.path.tilemap+tilemap_name+file.ext.image)
    
def unload_tilemap(tilemap_name:str) -> None|Err:
    tilemap_data = file.ask(file.path.tilemap+tilemap_name+file.ext.data)

    if __debug__ and tilemap_data == "notexixtant":
        tilemap_data.msg += " <- Wrong tilemap_data type"
        return tilemap_data
    
    if __debug__ and type(tilemap_data) != dict:
        return Err("notvalue", "Can't unload tilemap", f"Value : {tilemap_data}")
    
    for tile in tilemap_data["tiles"]:
        try:
            del tiles[tile]
        except KeyError:
            log.info(f"Tile {tile} already deleted")
    loaded_tilemaps.remove(tilemap_name)
    file.close(file.path.tilemap+tilemap_name+file.ext.data)

def unload_all_tilemaps() -> None:
    for tilemap_name in loaded_tilemaps:
        file.close(file.path.tilemap+tilemap_name+file.ext.data)
    loaded_tilemaps.clear()
    tiles.clear()

backgrounds:dict[pygame.surface.Surface] = {}
loaded_background = set()

def create_background(background_name:str) -> None|Err:
    background_data = file.ask(file.path.background+background_name+file.ext.data)

    if __debug__ and background_data == "notexixtant":
        background_data.msg += " <- Wrong background_data type"
        return background_data
    
    if __debug__ and type(background_data) != dict:
        return Err("notvalue", "Can't create background", f"Value : {background_data}")
    
    for background_tilemap in background_data["tilemaps"]:
        if background_tilemap not in loaded_tilemaps:
            load_tilemap(background_tilemap)

    background_tilesize = background_data["tile_size"]
    background_gridsizex, background_gridsizey = background_data["grid_size"]
    background_image = pygame.surface.Surface([background_tilesize*background_gridsizex, background_tilesize*background_gridsizey])
    background_tilset = []
    for tile in background_data["tiles"]:
        background_tilset.append(tiles[tile])

    if __debug__ and len(background_data["grid"])%(background_gridsizex*background_gridsizey)!=0:
        log.error(f"Background {background_name!r} faulty size")

    sequence = [
        (background_tilset[background_data["grid"][background_gridsizex*(grid*background_gridsizey+y)+x]-1], [x*background_tilesize, y*background_tilesize])
        for grid in range(len(background_data["grid"])//background_gridsizex//background_gridsizey)
        for y in range(background_gridsizey)
        for x in range(background_gridsizex)
        if background_data["grid"][background_gridsizex*(grid*background_gridsizey+y)+x] != 0 # skip if tile is empty
    ]
    background_image.blits(sequence)
    file.create(file.path.background+background_name+file.ext.image, data=background_image)
    file.write(file.path.background+background_name+file.ext.image)
    file.close(file.path.background+background_name+file.ext.data)
    file.close(file.path.background+background_name+file.ext.image)

def load_background(background_name:str) -> None|Err:
    backgrounds[background_name] = file.ask(file.path.background+background_name+file.ext.image)
    
    if __debug__ and backgrounds[background_name] == "notexistant":
        backgrounds[background_name].msg += " <- Wrong background_data type"
        return backgrounds.pop(background_name)

    if __debug__ and type(backgrounds[background_name]) != pygame.Surface:
        return Err("notvalue", "Can't load image", f"Value : {backgrounds.pop(background_name)}")

    if background_name not in loaded_background and backgrounds[background_name] != None:
        loaded_background.add(background_name)
    file.close(file.path.background+background_name+file.ext.image)

def unload_background(background_name:str) -> None:        
    del backgrounds[background_name]
    loaded_background.remove(background_name)

def unload_all_backgrounds() -> None:
    loaded_background.clear()
    backgrounds.clear()