# This a simple file (actually but after no) who is in charge of using the map.
import pygame, pytmx, pyscroll
from utils.storageHandler import param_get
from utils.consoleHandler import info

class sceneHandler:

    def __init__(self):
        # Creating the dictionary of maps in the scene and variables.
        self.maps = {}
        self.selected_map = None
        self.selected_scene = None

        info("Scene handler initialized")

    def quit(self):
        info("Scene handler has quit")

    def change_scene(self, scene_name=None):
        """Update the scene dictionnary with the new scene"""
        if scene_name is None:
            scene_name = self.selected_scene
        scene = param_get(scene_name, "scenes")

        for map_name in scene:
            # Load all the maps in scene
            self.maps[map_name] = {"file": scene[map_name]}
            self.maps[map_name]["tmx_data"] = pytmx.util_pygame.load_pygame("assets/scenes/" + self.maps[map_name]["file"]) # Setting here the scenes path
            self.maps[map_name]["map_data"] = pyscroll.TiledMapData(self.maps[map_name]["tmx_data"])

            # Get the walls and portals
            self.maps[map_name]["walls"] = {"solid": [], "sticky": [], "bouncy": []}
            self.maps[map_name]["portals"] = []
            for obj in self.maps[map_name]["tmx_data"].objects:
                if obj.type == "collision":
                    self.maps[map_name]["walls"][obj.properties["collision_type"]].append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                if obj.type == "portal":
                    self.maps[map_name]["portals"].append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            # Get the map_layer and set the zoom
            self.maps[map_name]["map_layer"] = pyscroll.orthographic.BufferedRenderer(self.map_data(map_name), param_get("screen_size"))
            screen_size = param_get("screen_size")
            if screen_size[0] < screen_size[1]:
                self.maps[map_name]["map_layer"].zoom = screen_size[1]*self.maps[map_name]["tmx_data"].get_layer_by_name("objects").properties["zoom"]/self.tmx_data(map_name).height/self.tmx_data(map_name).tileheight
            else:
                self.maps[map_name]["map_layer"].zoom = screen_size[0]*self.maps[map_name]["tmx_data"].get_layer_by_name("objects").properties["zoom"]/self.tmx_data(map_name).width/self.tmx_data(map_name).tilewidth

            # Get the player (not usefull in the future, it has to be in the save file)
            self.maps[map_name]["player"] = self.maps[map_name]["tmx_data"].get_object_by_name("player")

    # Fast functions
    def tmx_data(self, map_name=None):
        """Get the tmx data of the map (pytmx.TiledMap)"""
        if map_name is None:
            map_name = self.selected_map
        return self.maps[map_name]["tmx_data"]
    
    def map_data(self, map_name=None):
        """Get the map data of the map (pyscroll.TiledMapData)"""
        if map_name is None:
            map_name = self.selected_map
        return self.maps[map_name]["map_data"]
    
    def map_layer(self, map_name=None):
        """Get the map layer of the map (pyscroll.orthographic.BufferedRenderer)"""
        if map_name is None:
            map_name = self.selected_map
        return self.maps[map_name]["map_layer"]
    
    def walls(self, map_name=None):
        """Get the walls of the map (dict of list)"""
        if map_name is None:
            map_name = self.selected_map
        return self.maps[map_name]["walls"]
    
    def portals(self, map_name=None):
        """Get the player position of the map (list)"""
        if map_name is None:
            map_name = self.selected_map
        return self.maps[map_name]["portals"]
    
    def player(self, map_name=None):
        """Get the player position of the map (tuple)"""
        if map_name is None:
            map_name = self.selected_map
        return self.maps[map_name]["player"]
        
    def get_zoom(self, map_name=None):
        """Get the zoom of the map (float)"""
        if map_name is None:
            map_name = self.selected_map
        return self.maps[map_name]["map_layer"].zoom

# Set the console object
scene = sceneHandler()