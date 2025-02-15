import pygame, file, error

tiles = {}
loaded_tilemaps = set()

def load_tilemap(tilemap_name:str) -> None|error.Error:
    tilemap_data = file.ask(file.path.tilemap+tilemap_name+file.ext.data)
    tilemap_image = file.ask(file.path.tilemap+tilemap_name+file.ext.image)
    if error.is_group(tilemap_data, error.group.not_found):
        return error.Error(error.group.not_found, f"Can't load tilemap '{tilemap_name}', file '{file.path.tilemap+tilemap_name+file.ext.data}' not found")
    if error.is_group(tilemap_image, error.group.not_found):
        return error.Error(error.group.not_found, f"Can't load tilemap '{tilemap_name}', file '{file.path.tilemap+tilemap_name+file.ext.image}' not found")

    for tile in tilemap_data["tiles"]:
        if tile in tiles:
            return error.Error(error.group.already_done, f"Tile '{tile}' already loaded")
        
        tiles[tile] = tilemap_image.subsurface(tilemap_data["tiles"][tile][0]*tilemap_data["tile_size"], tilemap_data["tiles"][tile][1]*tilemap_data["tile_size"], tilemap_data["tile_size"], tilemap_data["tile_size"])
    loaded_tilemaps.add(tilemap_name)
    file.close(file.path.tilemap+tilemap_name+file.ext.image)
    
def unload_tilemap(tilemap_name:str) -> None|error.Error:
    tilemap_data = file.ask(file.path.tilemap+tilemap_name+file.ext.data)
    if error.is_group(tilemap_data, error.group.not_found):
        return error.Error(error.group.not_found, f"Can't unload tilemap '{tilemap_name}', file '{file.path.tilemap+tilemap_name+file.ext.data}' not found")
    
    for tile in tilemap_data["tiles"]:
        try:
            del tiles[tile]
        except KeyError:
            return error.Error(error.group.already_done, f"Tile {tile} already deleted")
    loaded_tilemaps.remove(tilemap_name)
    file.close(file.path.tilemap+tilemap_name+file.ext.data)

def unload_all_tilemaps() -> None:
    for tilemap_name in loaded_tilemaps:
        file.close(file.path.tilemap+tilemap_name+file.ext.data)
    loaded_tilemaps.clear()
    tiles.clear()


backgrounds:dict[pygame.surface.Surface] = {}
loaded_background = set()

def create_background(background_name:str) -> None|error.Error:
    background_data = file.ask(file.path.background+background_name+file.ext.data)
    if error.is_group(background_data, error.group.not_found):
        return error.Error(error.group.not_found, f"Can't create background '{background_name}', file '{file.path.background+background_name+file.ext.data}' not found")
    
    for background_tilemap in background_data["tilemaps"]:
        if background_tilemap not in loaded_tilemaps:
            load_tilemap(background_tilemap)
    background_tilesize = background_data["tile_size"]
    background_gridsizex, background_gridsizey = background_data["grid_size"]
    background_image = pygame.surface.Surface([background_tilesize*background_gridsizex, background_tilesize*background_gridsizey])
    background_tilset = []
    for tile in background_data["tiles"]:
        background_tilset.append(tiles[tile])
    sequence = [
        (background_tilset[tile-1], [x * background_tilesize, y * background_tilesize])
        for grid in background_data["grids"]
        for y, row in enumerate(grid)
        for x, tile in enumerate(row)
        if tile != 0 # skip if tile is empty
    ]
    background_image.blits(sequence)
    file.create(file.path.background+background_name+file.ext.image, data=background_image)
    file.write(file.path.background+background_name+file.ext.image)
    file.close(file.path.background+background_name+file.ext.data)
    file.close(file.path.background+background_name+file.ext.image)

def load_background(background_name:str) -> None:
    backgrounds[background_name] = file.ask(file.path.background+background_name+file.ext.image)
    if background_name not in loaded_background and backgrounds[background_name] != None:
        loaded_background.add(background_name)
    file.close(file.path.background+background_name+file.ext.image)

def unload_background(background_name:str) -> None:        
    del backgrounds[background_name]
    loaded_background.remove(background_name)

def unload_all_backgrounds() -> None:
    loaded_background.clear()
    backgrounds.clear()