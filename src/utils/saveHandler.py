from utils.storageHandler import param_get, param_reset, param_set
from utils.consoleSystem import warn

class saveHandler:
    
    def __init__(self):
        self.save_folder_path = "saves/"
        self.saves = param_get("saved", self.save_folder_path+"saved.json")
        self.selected_save = None

    def create_save(self, name):
        if name == None:
            name = self.selected_save
        param_reset(self.save_folder_path+name+".json")


save = saveHandler()
    
class SaveObject:

    def __init__(self, object):
        self.object = object

    def get_save(self, param):
        try:
            return param_get(self.object, save.saves[save.selected_save])[param]
        except:
            warn("No save named '"+str(save.selected_save)+"' was found.")
            return None

    def set_save(self, param, data):
        try:
            temp = param_get(self.object, save.saves[save.selected_save])
            temp[param] = data
            param_set(self.object, temp, save.saves[save.selected_save])
        except:
            warn("No save named '"+str(save.selected_save)+"' was found.")