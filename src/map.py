import pygame, file, error

tiles = {}
loaded_tilemaps = set()

def load_tilemap(tilemap_names:list[str]) -> list[error.Error]:
    err = []
    for tilemap_name in tilemap_names:
        tilemap_data, tilemap_image = file.ask([file.path.tilemap+tilemap_name+file.ext.data, file.path.tilemap+tilemap_name+file.ext.image])
        if error.is_error(tilemap_data, tilemap_image):
            err.append(error.Error(error.category.not_found, f"Can't load tilemap '{tilemap_name}', data or image file missing"))
            continue
    
        for tile in tilemap_data["tiles"]:
            if tile in tiles:
                err.append(error.Error(error.category.already_done, f"Tile '{tile}' already loaded"))
            
            tiles[tile] = tilemap_image.subsurface(tilemap_data["tiles"][tile][0]*tilemap_data["tile_size"], tilemap_data["tiles"][tile][1]*tilemap_data["tile_size"], tilemap_data["tile_size"], tilemap_data["tile_size"])
        loaded_tilemaps.add(tilemap_name)
        file.close([file.path.tilemap+tilemap_name+file.ext.image])
    return err
    
def unload_tilemap(tilemap_names:list[str]) -> list[error.Error]:
    err = []
    for tilemap_name in tilemap_names:
        tilemap_data, = file.ask([file.path.tilemap+tilemap_name+file.ext.data])
        if error.is_error(tilemap_data):
            err.append(error.Error(error.category.not_found, f"Can't unload tilemap '{tilemap_name}', data file missing"))
            continue
        
        for tile in tilemap_data["tiles"]:
            try:
                del tiles[tile]
            except KeyError:
                err.append(error.Error(error.category.already_done, f"Tile {tile} already deleted"))
        loaded_tilemaps.remove(tilemap_name)
        file.close([file.path.tilemap+tilemap_name+file.ext.data])
    return err

backgrounds:dict[pygame.surface.Surface] = {}
loaded_background = set()

    
def create_background(background_names:list[str]) -> list[error.Error]:
    err = []
    for background_name in background_names:
        background_data, = file.ask([file.path.background+background_name+file.ext.data])
        if error.is_error(background_data):
            err.append(error.Error(error.category.not_found, f"Can't create background '{background_name}', data file missing"))
            continue
        
        load_tilemap([background_tilemap for background_tilemap in background_data["tilemaps"] if background_tilemap not in loaded_tilemaps])
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
        file.create([file.path.background+background_name+file.ext.image], data=background_image)
        file.write([file.path.background+background_name+file.ext.image])
        file.close([file.path.background+background_name+file.ext.data, file.path.background+background_name+file.ext.image])
    return err

def load_background(background_names:list[str]) -> None:
    for background_name in background_names:
        backgrounds[background_name], = file.ask([file.path.background+background_name+file.ext.image])
        if background_name not in loaded_background and backgrounds[background_name] != None:
            loaded_background.add(background_name)
        file.close([file.path.background+background_name+file.ext.image])

def unload_background(background_names:list[str]) -> None:
    for background_name in background_names:          
        del backgrounds[background_name]
        loaded_background.remove(background_name)