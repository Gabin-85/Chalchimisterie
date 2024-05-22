from utils.resourcesHandler import save

class entityHandler:
    
    def __init__(self):
        self.entities = []
        self.shown_entities = []
        self.loaded_scenes = []
        self.need_update = True

    def quit(self):
        save.set("loaded_scenes", self.loaded_scenes)

entity_handler = entityHandler()