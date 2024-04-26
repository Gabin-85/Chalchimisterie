# This a simple file (actually but after no) who is in charge of using the map.
import pygame, pytmx, pyscroll
from utils.storageHandler import param_get

class sceneHandler:

    def __init__(self):
        # Creating the dictionary of maps in the scene
        self.maps = {}
        self.map_name = None
        self.scene_name = None

    def change_scene(self, scene_name=None):
        """Update the scene dictionnary with the new scene"""
        if scene_name is None:
            scene_name = self.scene_name
        scene = param_get(scene_name, "scenes")

        # Create a dict named scene where all the map data is stored
        for map_name in scene:
            self.maps[map_name] = {"file": scene[map_name]}
            self.maps[map_name]["tmx_data"] = pytmx.util_pygame.load_pygame("assets/scenes/" + self.maps[map_name]["file"])
            self.maps[map_name]["map_data"] = pyscroll.TiledMapData(self.maps[map_name]["tmx_data"])

            self.maps[map_name]["walls"] = {"solid": [], "sticky": [], "bouncy": []}
            for obj in self.maps[map_name]["tmx_data"].objects:
                if obj.name == "collision":
                    self.maps[map_name]["walls"][obj.type].append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            self.maps[map_name]["portals"] = []
            for obj in self.maps[map_name]["tmx_data"].objects:
                if obj.name == "portal":
                    self.maps[map_name]["portals"].append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            self.maps[map_name]["player"] = self.maps[map_name]["tmx_data"].get_object_by_name("player")

    def get_map_zoom(self):
        """Get the zoom with the screen size, the zoom of the map, and the size of the map"""
        screen_size = param_get("screen_size")
    # Get the real zoom
        if screen_size[0] < screen_size[1]:
            map_zoom = screen_size[1]*self.maps[self.map_name]["tmx_data"].get_layer_by_name("objects").properties["zoom"]/(self.tmx_data().height*self.tmx_data().tileheight)
        else:
            map_zoom = screen_size[0]*self.maps[self.map_name]["tmx_data"].get_layer_by_name("objects").properties["zoom"]/(self.tmx_data().width*self.tmx_data().tilewidth)
        return map_zoom

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
    
scene = sceneHandler()