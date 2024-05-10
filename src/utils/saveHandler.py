from utils.resourcesHandler import resourcesHandler
from utils.consoleSystem import warn, exception

class saveHandler(resourcesHandler):

    def __init__(self) -> None:
        super().__init__("saves", None)
        self.selected_save = None

    def quit(self):
        saves = list(self.loaded_files.keys())
        for save in saves:
            self.unload_file(save)
save = saveHandler()

class saveEntity:

    def __init__(self, id:int) -> None:
        # Setting up the identity
        self.id = id
        self.data = None

    def load(self):
        try:
            self.data = save.loaded_files[save.selected_save]["data"]["entity"][self.id]
            return True
        except Exception as e:
            warn("Can't load entity '"+str(id)+"' from save '"+str(save.selected_save)+"'.")
            exception(e)
            return False
        
    def create(self):
        try:
            save.loaded_files[save.selected_save]["data"]["entity"][self.id] = {}
            self.load()
            return True
        except Exception as e:
            warn("Can't create entity '"+str(id)+"' in save '"+str(save.selected_save)+"'.")
            exception(e)
            return False
        
    def unload(self):
        try:
            save.loaded_files[save.selected_save]["data"]["entity"][self.id] = self.data
            return True
        except Exception as e:
            warn("Can't unload entity '"+str(id)+"' in save '"+str(save.selected_save)+"'.")
            exception(e)
            return False

    def get(self, parameter:str):
        try:
            return self.data[parameter]
        except Exception as e:
            warn("Can't get parameter '"+str(parameter)+"' from entity '"+str(id)+"' in save '"+str(save.selected_save)+"'.")
            exception(e)
            return None
    
    def set(self, parameter:str, value:any):
        try:
            self.data[parameter] = value
            return True
        except Exception as e:
            warn("Can't set parameter '"+str(parameter)+"' in entity '"+str(id)+"' in save '"+str(save.selected_save)+"'.")
            exception(e)
            return False