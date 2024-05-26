from utils.resourcesHandler import save

class entityHandler:
    
    def __init__(self):
        self.entities = []
        self.shown_entities = save.get("shown_entities")
        self.loaded_scenes = save.get("loaded_scenes")
        self.need_update = True

    def quit(self):
        save.set("shown_entities", self.shown_entities)
        save.set("loaded_scenes", self.loaded_scenes)

    def update_shown_entities(self, scene_name, map_name):
        self.shown_entities = [entity.general_data["id"] for entity in self.entities if entity.general_data["map_name"] == map_name and entity.general_data["scene_name"] == scene_name]
        self.need_update = False

    def get_entities(self):
        return [entity for entity in self.entities if entity.general_data["id"] in self.shown_entities]

entity_handler = entityHandler()