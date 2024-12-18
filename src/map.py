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
            tilemap_data:dict = file.ask(path.tilemap+tilemap_name+ext.data)
            tilemap_image:pygame.surface.Surface = file.ask(path.tilemap+tilemap_name+ext.image)

            if tilemap_data == None or tilemap_image == None:
                console.warn(f"Can't load tilemap '{tilemap_name}'. Data or image file missing.")
                return
        
            for tile in tilemap_data["tiles"]:
                if tilemap_name not in tilemap.loaded_tilemaps and tile in tilemap.tiles:
                    console.warn(f"Tile '{tile}' already loaded by another tilemap.")
                
                tilemap.tiles[tile] = tilemap_image.subsurface(tilemap_data["tiles"][tile][0]*tilemap_data["tilesize"], tilemap_data["tiles"][tile][1]*tilemap_data["tilesize"], tilemap_data["tilesize"], tilemap_data["tilesize"])

            tilemap.loaded_tilemaps.append(tilemap_name)
        
    @staticmethod
    def unload(*tilemap_names:str) -> None:
        """
        Unload tilemaps

        Args:
            tilemap_names (str): The tilemaps names
        """
        for tilemap_name in tilemap_names:
            tilemap_data:dict = file.ask(path.tilemap+tilemap_name+ext.data)

            if tilemap_data == None:
                console.warn(f"Can't unload tilemap '{tilemap_name}'. Data file missing.")
                return
            
            for tile in tilemap_data["tiles"]:
                if tilemap.tiles[tile]:
                    del tilemap.tiles[tile]

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
            if file.find(path.background+background_name+ext.image):
                background.backgrounds[background_name] = file.ask(path.background+background_name+ext.image)
                background.loaded_background.append(background_name)
            
            else:
                background.create(background_name)

    @staticmethod
    def create(*background_names:str) -> None:
        """
        Create backgrounds

        Args:
            background_names: The backgrounds names
        """
        for background_name in background_names:
            background_data = file.ask(path.background+background_name+ext.data)

            if background_data == None:
                console.warn(f"Can't load background '{background_name}'. Data file missing.")
                return
                    
            background_image = pygame.surface.Surface([background_data["tilesize"]*background_data["size"][0], background_data["tilesize"]*background_data["size"][1]])

            for needed_tilemap in background_data["needed_tilemaps"]:
                if needed_tilemap not in tilemap.loaded_tilemaps:
                    tilemap.load(needed_tilemap)
                    
            backgroud_tilset = []
            for tile in background_data["tiles"]:
                backgroud_tilset.append(tilemap.tiles[tile])

            for grid in background_data["grids"]:
                for y in range(background_data["size"][1]):
                    for x in range(background_data["size"][0]):
                        background_image.blit(backgroud_tilset[grid[y][x]], [x*background_data["tilesize"], y*background_data["tilesize"]])

            file.create(path.background+background_name+ext.image)
            file.files[path.background+background_name+ext.image] = background_image
            file.write(path.background+background_name+ext.image)

            background.backgrounds[background_name] = background_image
            background.loaded_background.append(background_name)




    @staticmethod
    def unload(*background_names:str) -> None:
        """
        Unload backgrounds

        Args:
            background_names: The backgrounds names
        """
        pass