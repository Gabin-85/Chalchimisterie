# This file handle the loads of the scenes and the maps.
import pytmx, pyscroll
from utils.mathToolbox import Vector2D, Rect2D
from utils.resourcesHandler import save
from utils.resourcesHandler import storage
from utils.entityHandler import entity_handler
from utils.entityToolbox import Entity
from utils.consoleSystem import warn, info, debug, trace, exception

class loadHandler:

    def __init__(self):
        # Creating the dictionary of maps in the scene and variables.
        self.scene_folder_path = "assets/scenes/" # Setting here the scenes path
        self.selected_save = None
        self.selected_scene = None
        self.selected_map = None
        self.scenes = {}

        info("Scene handler initialized.")

    def quit(self):
        """Quit the scene handler"""
        del self.scene_folder_path
        del self.selected_save
        del self.selected_scene
        del self.selected_map
        del self.scenes
        info("Scene handler has quit.")
        
    ##########
    # Scenes #
    ##########

    def load_scene(self, scene_name:str=None):
        """Generate a scene"""
        if scene_name is None:
            scene_name = self.selected_scene
        scene_path = storage.get(scene_name, "scenes")

        if scene_path is None:
            warn("Scene '"+scene_name+"' not found.")
            return False
        
        self.scenes[scene_name] = {}
        for map_name in scene_path:
            # Load all the maps in scene
            self.scenes[scene_name][map_name] = {"file": scene_path[map_name]}
            try:
                self.scenes[scene_name][map_name]["tmx_data"] = pytmx.util_pygame.load_pygame(self.scene_folder_path + self.scenes[scene_name][map_name]["file"])
            except Exception as e:
                warn("Map named '"+self.scenes[scene_name][map_name]["file"]+"' not found. Abort load.")
                exception(e)
                return False
            self.scenes[scene_name][map_name]["map_data"] = pyscroll.TiledMapData(self.scenes[scene_name][map_name]["tmx_data"])

            # Get the walls and portals
            self.scenes[scene_name][map_name]["walls"] = []
            self.scenes[scene_name][map_name]["portals"] = {}
            self.scenes[scene_name][map_name]["portals_exits"] = {}
            self.scenes[scene_name][map_name]["entities_pattern"] = []
            for obj in self.scenes[scene_name][map_name]["tmx_data"].objects:
                match obj.type:
                    case "collision":
                        self.scenes[scene_name][map_name]["walls"].append({
                            "rect": Rect2D(obj.x, obj.y, obj.width, obj.height),
                            "collision_type": obj.properties["collision_type"]})
                    case "portal":
                        self.scenes[scene_name][map_name]["portals"][obj.name] = {
                            "rect":Rect2D(obj.x, obj.y, obj.width, obj.height),
                            "targeted_scene_name": obj.properties["targeted_scene_name"],
                            "targeted_map_name": obj.properties["targeted_map_name"],
                            "targeted_exit_name": obj.properties["targeted_exit_name"]}
                    case "portal_exit":
                        self.scenes[scene_name][map_name]["portals_exits"][obj.name] = self.scenes[scene_name][map_name]["tmx_data"].get_object_by_name(obj.name)
                    case "entity":
                        self.scenes[scene_name][map_name]["entities_pattern"].append({
                            "position":[obj.x, obj.y],
                            "name": obj.name,
                            "pattern": obj.properties["pattern"]})

            # Get the map_layer and set the zoom
            self.scenes[scene_name][map_name]["map_layer"] = pyscroll.orthographic.BufferedRenderer(self.get_map_data(map_name, scene_name), storage.get("screen_size"))
            screen_size = storage.get("screen_size")
            if screen_size[0] < screen_size[1]:
                self.scenes[scene_name][map_name]["map_layer"].zoom = screen_size[1]*self.scenes[scene_name][map_name]["tmx_data"].get_layer_by_name("objects").properties["zoom"]/self.get_tmx_data(map_name, scene_name).height/self.get_tmx_data(map_name, scene_name).tileheight
            else:
                self.scenes[scene_name][map_name]["map_layer"].zoom = screen_size[0]*self.scenes[scene_name][map_name]["tmx_data"].get_layer_by_name("objects").properties["zoom"]/self.get_tmx_data(map_name, scene_name).width/self.get_tmx_data(map_name, scene_name).tilewidth

            # Check the entities in the scenes are in the save
            if scene_name in entity_handler.loaded_scenes:
                # If yes load all entities
                for entity in save.get("entities"):
                    if entity["map_name"] == map_name and entity["scene_name"] == scene_name:
                        entity_handler.entities.append(Entity())
                        entity_handler.entities[-1].load(entity["id"])
            else:
                # If not create and add all entities
                for entity in self.get_entities_pattern(map_name, scene_name):
                    entity_handler.entities.append(Entity())
                    entity_handler.entities[-1].create(entity["name"], entity["pattern"], scene_name, map_name, Vector2D(*entity["position"]))
            
        if scene_name not in entity_handler.loaded_scenes:
            entity_handler.loaded_scenes.append(scene_name)

        trace("'"+scene_name+"' loaded!")
        return True
    
    def unload_scene(self, scene_name=None):
        """Delete all maps from the dictionnary that are in the scene"""

        # Get all maps in scene
        if scene_name is None:
            scene_name = self.selected_scene

        if scene_name in self.scenes:
            del self.scenes[scene_name]
            trace("'"+scene_name+"' unloaded!")
            return True
        else:
            return False
        
    def scene_cleanup(self):
        """Unload all used scenes"""
        scenes = self.loaded_scenes()
        for scene in scenes:
            if scene != self.selected_scene:
                self.unload_scene(scene)
        debug("Cleanup scene.")
            
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
        return list(self.scenes.keys())

    def has_scene_load(self, scene_name=None):
        """Give the number of maps in the scene, if 0 then the scene is not loaded"""
        if scene_name is None:
            scene_name = self.selected_scene
        if scene_name in self.scenes:
            return len(self.scenes[scene_name])
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
        return self.scenes[scene_name][map_name]["map_layer"].zoom

    def get_tmx_data(self, map_name=None, scene_name=None):
        """Get the tmx data of the map (pytmx.TiledMap)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.scenes[scene_name][map_name]["tmx_data"]
    
    def get_map_data(self, map_name=None, scene_name=None):
        """Get the map data of the map (pyscroll.TiledMapData)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.scenes[scene_name][map_name]["map_data"]
    
    def get_map_layer(self, map_name=None, scene_name=None):
        """Get the map layer of the map (pyscroll.orthographic.BufferedRenderer)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.scenes[scene_name][map_name]["map_layer"]
    
    def get_walls(self, map_name=None, scene_name=None):
        """Get the walls of the map (list)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.scenes[scene_name][map_name]["walls"]
    
    def get_portals(self, map_name=None, scene_name=None):
        """Get the player position of the map (list)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.scenes[scene_name][map_name]["portals"]
    
    def get_portal_exit(self, portals):
        """Get the portal_exit of a portal"""
        if self.has_scene_load(portals["targeted_scene_name"]) == 0:
            trace("Scene '"+portals["targeted_scene_name"]+"' not loaded.")
            self.load_scene(portals["targeted_scene_name"])
        return self.scenes[portals["targeted_scene_name"]][portals["targeted_map_name"]]["portals_exits"][portals["targeted_exit_name"]]
    
    def get_entities_pattern(self, map_name=None, scene_name=None):
        """Get the entities pattern of the map (list)"""
        if scene_name is None:
            scene_name = self.selected_scene
        if self.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            self.load_scene(scene_name)
        if map_name is None:
            map_name = self.selected_map
        return self.scenes[scene_name][map_name]["entities_pattern"]


# Set the console object
load = loadHandler()