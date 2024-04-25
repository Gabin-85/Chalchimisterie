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

    def __init__(self):
        # Creating the scene dictionary
        self.maps = {}

        # Create a dict of scenes where all the map data is stored
        all_scenes = param_get("scenes", "scenes")
        for scene_name in all_scenes:
            self.maps[scene_name] = {"file": all_scenes[scene_name]}
            self.maps[scene_name]["tmx_data"] = pytmx.util_pygame.load_pygame("assets/scenes/" + self.maps[scene_name]["file"])
            self.maps[scene_name]["map_data"] = pyscroll.TiledMapData(self.maps[scene_name]["tmx_data"])

            self.maps[scene_name]["walls"] = []
            for obj in self.maps[scene_name]["tmx_data"].objects:
                if obj.type == "collision":
                    self.maps[scene_name]["walls"].append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            print(self.maps)