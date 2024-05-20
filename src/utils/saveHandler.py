
from utils.consoleSystem import warn, info, debug, trace, exception
from utils.resourcesHandler import save

class saveHandler():

    def __init__(self):
        """Init the save handler"""
        self.entities = []
        self.save = {}

        info("Save handler initialized.")

    def setup(self, save_name:str):
        try:
            if save_name in save.paths:
                self.load_save(save_name)
            else:
                self.generate_save(save_name)
            debug("Saver has selected save '"+save_name+"'.")
        except Exception as e:
            warn("Can't select save '"+save_name+"'.")
            exception(e)

    def quit(self):
        """Quit the save handler"""
        # Add all save object
        self.save["entities"] = self.entities
        save.write_file(self.selected_save, self.save)

        del self.entities
        del self.save

        info("Save handler has quit.")

    def load_save(self, save_name:str):
        """Load a save"""
        try:
            self.selected_save, save.handler_default = save_name, save_name
            self.save = save.read_file(self.selected_save)
            self.entities = []

            trace("Save '"+self.selected_save+"' loaded.")
            return True
        except Exception as e:
            warn("Can't load save '"+self.selected_save+"'.")
            exception(e)
            return False

    def generate_save(self, save_name:str):
        """Generate a save (scenes, entities, ...)"""
        try:
            self.selected_save, save.handler_default = save_name, save_name
            self.save = {"entities": []}
            save.create_file(self.selected_save, "json")

            trace("Save '"+self.selected_save+"' generated.")
            return True
        except Exception as e:
            warn("Can't generate save '"+self.selected_save+"'.")
            exception(e)
            return False
        
    def unload_save(self):
        """Unload a save"""

        try:
            self.save["entities"] = self.entities
            save.write_file(self.selected_save, self.save)
            self.save = {}

            trace("Save '"+self.selected_save+"' unloaded.")
            return True
        except Exception as e:
            warn("Save '"+self.selected_save+"' not found. Abort unload.")
            exception(e)
            return False
        
    def delete_save(self):
        """Delete a save"""

        try:
            self.unload_save(self.selected_save)
            save.delete_file(self.selected_save)

            trace("Save '"+self.selected_save+"' deleted.")
            return True
        except Exception as e:
            warn("Save '"+self.selected_save+"' not found. Abort delete.")
            exception(e)
            return False
        
    def get_entities(self, map_name=None, scene_name=None):
        """Get the entities of the map (also load all entities if the map has never benn loaded)"""
        from utils.loadHandler import load
        
        if scene_name is None:
            scene_name = load.selected_scene
        if load.has_scene_load(scene_name) == 0:
            trace("Scene '"+scene_name+"' not loaded.")
            load.load_scene(scene_name)
        if map_name is None:
            map_name = load.selected_map
        
        return [entity for entity in saver.entities if entity.map_name == map_name and entity.scene_name == scene_name]

saver = saveHandler()