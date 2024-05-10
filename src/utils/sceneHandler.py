# This file handle the loads of the scenes and the maps.
import pygame, pytmx, pyscroll
from utils.resourcesHandler import param_get
from utils.consoleSystem import warn, info, debug, trace

class sceneHandler:

    def __init__(self):
        # Creating the dictionary of maps in the scene and variables.
        self.scene_folder_path = "assets/scenes/" # Setting here the scenes path
        self.data = {}
        self.selected_map = None
        self.selected_scene = None

        info("Scene handler initialized.")

    def quit(self):
        info("Scene handler has quit.")

    ##########
    # SCENES #
    ##########

    def load_scene(self, scene_name=None):
        """Add the maps from the scene in the dictionnary"""
        
        # Get all maps in scene
        if scene_name is None:
            scene_name = self.selected_scene
        scene = param_get(scene_name, "scenes")

        if scene == None:
            warn("Scene '"+scene_name+"' not found.")
            return False
        self.data[scene_name] = {}
        for map_name in scene:
            # Load all the maps in scene
            self.data[scene_name][map_name] = {"file": scene[map_name]}
            try:
                self.data[scene_name][map_name]["tmx_data"] = pytmx.util_pygame.load_pygame(self.scene_folder_path + self.data[scene_name][map_name]["file"])
            except FileNotFoundError:
                warn("Map named '"+self.data[scene_name][map_name]["file"]+"' not found. Abort load.")
                return False
            self.data[scene_name][map_name]["map_data"] = pyscroll.TiledMapData(self.data[scene_name][map_name]["tmx_data"])

            # Get the walls and portals
            self.data[scene_name][map_name]["walls"] = []
            self.data[scene_name][map_name]["portals"] = {}
            self.data[scene_name][map_name]["portals_exits"] = {}
            for obj in self.data[scene_name][map_name]["tmx_data"].objects:
                match obj.type:
                    case "collision":
                        self.data[scene_name][map_name]["walls"].append({
                            "rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                            "collision_type": obj.properties["collision_type"]})
                    case "portal":
                        self.data[scene_name][map_name]["portals"][obj.name] = {
                            "rect":pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                            "targeted_scene_name": obj.properties["targeted_scene_name"],
                            "targeted_map_name": obj.properties["targeted_map_name"],
                            "targeted_exit_name": obj.properties["targeted_exit_name"]}
                    case "portal_exit":
                        self.data[scene_name][map_name]["portals_exits"][obj.name] = self.data[scene_name][map_name]["tmx_data"].get_object_by_name(obj.name)

            # Get the map_layer and set the zoom
            self.data[scene_name][map_name]["map_layer"] = pyscroll.orthographic.BufferedRenderer(self.get_map_data(map_name, scene_name), param_get("screen_size"))
            screen_size = param_get("screen_size")
            if screen_size[0] < screen_size[1]:
                self.data[scene_name][map_name]["map_layer"].zoom = screen_size[1]*self.data[scene_name][map_name]["tmx_data"].get_layer_by_name("objects").properties["zoom"]/self.get_tmx_data(map_name, scene_name).height/self.get_tmx_data(map_name, scene_name).tileheight
            else:
                self.data[scene_name][map_name]["map_layer"].zoom = screen_size[0]*self.data[scene_name][map_name]["tmx_data"].get_layer_by_name("objects").properties["zoom"]/self.get_tmx_data(map_name, scene_name).width/self.get_tmx_data(map_name, scene_name).tilewidth
            
        trace("'"+scene_name+"' loaded!")
        return True

    def unload_scene(self, scene_name=None):
        """Delete all maps from the dictionnary that are in the scene"""

        # Get all maps in scene
        if scene_name is None:
            scene_name = self.selected_scene

        if scene_name in self.data:
            del self.data[scene_name]
            trace("'"+scene_name+"' unloaded!")
            return True
        else:
            return False
        
    def scene_cleanup(self):
        """Unload all used scenes"""
        scenes = self.loaded_scenes()
        if self.selected_scene in scenes:
            scenes.remove(self.selected_scene)
        if len(scenes) != 0:
            debug("Cleanup scene.")
            for scene in scenes:
                self.unload_scene(scene)
            
    def change_scene(self, scene_name=None):
        """Unload all scenes and load the one given in the parameter"""
        if scene_name is None:
            scene_name = self.selected_scene
        self.selected_scene = scene_name
        
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)

    def loaded_scenes(self):
        """Get all the loaded scenes"""
        return list(self.data.keys())

    def has_scene_load(self, scene_name=None):
        """Give the number of maps in the scene, if 0 then the scene is not loaded"""
        if scene_name is None:
            scene_name = self.selected_scene
        if scene_name in self.data:
            return len(self.data[scene_name])
        else:
            return 0
        
    ########
    # MAPS #
    ########
        
    def change_map(self, map_name=None, scene_name=None):
        """Unset the current map and load the one given in the parameter"""
        self.change_scene(scene_name)

        if map_name is None:
            map_name = self.selected_map
        self.selected_map = map_name

    ###########
    # GETTERS #
    ###########

    def get_zoom(self, map_name=None, scene_name=None):
        """Get the zoom of the map (float)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.data[scene_name][map_name]["map_layer"].zoom

    def get_tmx_data(self, map_name=None, scene_name=None):
        """Get the tmx data of the map (pytmx.TiledMap)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.data[scene_name][map_name]["tmx_data"]
    
    def get_map_data(self, map_name=None, scene_name=None):
        """Get the map data of the map (pyscroll.TiledMapData)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.data[scene_name][map_name]["map_data"]
    
    def get_map_layer(self, map_name=None, scene_name=None):
        """Get the map layer of the map (pyscroll.orthographic.BufferedRenderer)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.data[scene_name][map_name]["map_layer"]
    
    def get_walls(self, map_name=None, scene_name=None):
        """Get the walls of the map (list)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.data[scene_name][map_name]["walls"]
    
    def get_portals(self, map_name=None, scene_name=None):
        """Get the player position of the map (list)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.data[scene_name][map_name]["portals"]
    
    def get_portal_exit(self, portals):
        """Get the portal_exit of a portal"""
        if self.has_scene_load(portals["targeted_scene_name"]) == 0:
            trace("Scene '"+portals["targeted_scene_name"]+"' not loaded.")
            self.load_scene(portals["targeted_scene_name"])
        return self.data[portals["targeted_scene_name"]][portals["targeted_map_name"]]["portals_exits"][portals["targeted_exit_name"]]

# Set the console object
scene = sceneHandler()