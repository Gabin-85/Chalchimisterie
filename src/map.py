from utils.console import console
from args import path, ext
from utils.file import file
import pygame

class tilemap():

    tiles = {}
    loaded_tilemaps = []

    @staticmethod
    def load(*tilemap_names:str) -> None:
        """
        Load tilemaps

        Args:
            tilemap_names (str): The tilemaps names
        """
        for tilemap_name in tilemap_names:
            tilemap_data, tilemap_image = file.ask(path.tilemap+tilemap_name+ext.data, path.tilemap+tilemap_name+ext.image)

            if tilemap_data == None  or tilemap_image == None:
                console.warn(f"Can't load tilemap '{tilemap_name}'. Data or image file missing.")
                continue
        
            for tile in tilemap_data["tiles"]:
                if tile in tilemap.tiles:
                    console.warn(f"Tile '{tile}' already loaded.")
                
                tilemap.tiles[tile] = tilemap_image.subsurface(tilemap_data["tiles"][tile][0]*tilemap_data["tile_size"], tilemap_data["tiles"][tile][1]*tilemap_data["tile_size"], tilemap_data["tile_size"], tilemap_data["tile_size"])

            tilemap.loaded_tilemaps.append(tilemap_name)
        
    @staticmethod
    def unload(*tilemap_names:str) -> None:
        """
        Unload tilemaps

        Args:
            tilemap_names (str): The tilemaps names
        """
        for tilemap_name in tilemap_names:
            tilemap_data, = file.ask(path.tilemap+tilemap_name+ext.data)

            if tilemap_data == None:
                console.warn(f"Can't unload tilemap '{tilemap_name}'. Data file missing.")
                continue
            
            for tile in tilemap_data["tiles"]:
                try:
                    del tilemap.tiles[tile]
                except KeyError:
                    pass

            tilemap.loaded_tilemaps.remove(tilemap_name)
            file.close(path.tilemap+tilemap_name+ext.data)
            file.close(path.tilemap+tilemap_name+ext.image)

class background():

    backgrounds:dict[pygame.surface.Surface] = {}
    loaded_background:list = []

    @staticmethod
    def load(*background_names:str) -> None:
        """
        Load backgrounds

        Args:
            background_names: The backgrounds names
        """
        for background_name in background_names:
            background.backgrounds[background_name], = file.ask(path.background+background_name+ext.image)
            if background.backgrounds[background_name] == None:
                background.create(background_name)
            else:
                background.loaded_background.append(background_name)

    @staticmethod
    def create(*background_names:str) -> None:
        """
        Create backgrounds

        Args:
            background_names: The backgrounds names
        """
        for background_name in background_names:
            background_data, = file.ask(path.background+background_name+ext.data)

            if background_data == None:
                console.warn(f"Can't create background '{background_name}'. Data file missing.")
                continue
            
            for background_tilemap in background_data["tilemaps"]:
                if background_tilemap not in tilemap.loaded_tilemaps:
                    tilemap.load(background_tilemap)

            background_image = pygame.surface.Surface([background_data["tile_size"]*background_data["grid_size"][0], background_data["tile_size"]*background_data["grid_size"][1]])
   
            background_tilset = []
            for tile in background_data["tiles"]:
                background_tilset.append(tilemap.tiles[tile])

            for grid in background_data["grids"]:
                try:
                    for y in range(background_data["grid_size"][1]):
                        for x in range(background_data["grid_size"][0]):
                            background_image.blit(background_tilset[grid[y][x]], [x*background_data["tile_size"], y*background_data["tile_size"]])
                except IndexError:
                    console.warn(f"Incompactible grid sizes in background '{background_name}'.")

            file.create(path.background+background_name+ext.image)
            file.files[path.background+background_name+ext.image] = background_image

            background.backgrounds[background_name] = background_image
            background.loaded_background.append(background_name)

    @staticmethod
    def unload(*background_names:str) -> None:
        """
        Unload backgrounds

        Args:
            background_names: The backgrounds names
        """
        for background_name in background_names:          
            del background.backgrounds[background_name]
            del background.loaded_background[background.loaded_background.index(background_name)]
            
            file.write(path.background+background_name+ext.image)
            file.close(path.background+background_name+ext.data)
                