# This a simple file (actually but after no) who is in charge of using the map.
import pygame, pytmx, pyscroll
from utils.storageHandler import *
from utils.consoleHandler import *

def get_map_zoom(zoom, screen_width, screen_height):
    # Get the real zoom
        if screen_width < screen_height:
            map_zoom = screen_height/1600*zoom
        else:
            map_zoom = screen_width/1600*zoom
        return map_zoom

class sceneHandler:

    def __init__(self, scene_name, map_name):
        # Creating the dictionary of maps in the scene
        self.maps = {}
        self.map_name = map_name
        self.scene_name = scene_name
        self.change_scene()

    def change_scene(self, scene_name=None):
        """Update the scene dictionnary with the new scene"""
        if scene_name is not None:
            self.scene_name = scene_name
        scene = param_get(self.scene_name, "scenes")

        # Create a dict named scene where all the map data is stored
        for self.map_name in scene:
            self.maps[self.map_name] = {"file": scene[self.map_name]}
            self.maps[self.map_name]["tmx_data"] = pytmx.util_pygame.load_pygame("assets/scenes/" + self.maps[self.map_name]["file"])
            self.maps[self.map_name]["map_data"] = pyscroll.TiledMapData(self.maps[self.map_name]["tmx_data"])

            self.maps[self.map_name]["walls"] = {"solid": [], "sticky": [], "bouncy": []}
            for obj in self.maps[self.map_name]["tmx_data"].objects:
                if obj.name == "collision":
                    self.maps[self.map_name]["walls"][obj.type].append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            self.maps[self.map_name]["portals"] = []
            for obj in self.maps[self.map_name]["tmx_data"].objects:
                if obj.name == "portal":
                    self.maps[self.map_name]["portals"].append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            self.maps[self.map_name]["player"] = self.maps[self.map_name]["tmx_data"].get_object_by_name("player")

    # Fast functions
    def tmx_data(self):
        """Get the tmx data of the map (pytmx.TiledMap)"""
        return self.maps[self.map_name]["tmx_data"]
    
    def map_data(self):
        """Get the map data of the map (pyscroll.TiledMapData)"""
        return self.maps[self.map_name]["map_data"]
    
    def walls(self):
        """Get the walls of the map (dict of list)"""
        return self.maps[self.map_name]["walls"]
    
    def portals(self):
        """Get the player position of the map (list)"""
        return self.maps[self.map_name]["portals"]
    
    def player(self):
        """Get the player position of the map (tuple)"""
        return self.maps[self.map_name]["player"]