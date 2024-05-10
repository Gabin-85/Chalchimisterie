from utils.consoleSystem import warn
import json

class saveHandler:

    def __init__(self) -> None:
        self.save_folder_path = "resources/saves/"
        self.selected_save = None
        self.data = {}

    def quit(self):
        saves = list(self.data.keys())
        for save in saves:
            self.unload_save(save)

    def load_save(self, save_name:str):
        if save_name is None:
            save_name = self.selected_save
        if self.selected_save is None:
            self.selected_save = save_name

        try:
            # Loading the save
            with open(self.save_folder_path+save_name+".json", "r") as file:
                self.data[save_name] = json.load(file)
        except:
            warn("No save named '"+str(save_name)+"' was found.")

    def unload_save(self, save_name:str=None):
        if save_name is None:
            save_name = self.selected_save
        
        try:
            # Saving the save
            with open(self.save_folder_path+save_name+".json", "w") as file:
                json.dump(self.data[save_name], file, indent=4)
            # Deleting the live save
            del self.data[save_name]
            if self.selected_save == save_name:
                self.selected_save = None
        except:
            warn("Can't unload save named '"+str(save_name)+"'.")

    def create_save(self, save_name:str):
        try:
            with open(self.save_folder_path+save_name+".json", "w") as file:
                file.write('{"entity":[]}')
            self.load_save(save_name)
        except:
            warn("Can't create save named '"+str(save_name)+"'.")
saver = saveHandler()

class saveObject:

    def __init__(self, type:str, id:int) -> None:
        # Setting up the identity
        self.type = type
        self.id = id
        self.data = None

        if self.id > len(saver.data[saver.selected_save][self.type]):
            saver.data[saver.selected_save][self.type][self.id] = {}

    def load(self):
        try:
            self.data = saver.data[saver.selected_save][self.type][self.id]
        except:
            warn("The save "+saver.selected_save+" don't have an object of type "+self.type+" with id "+self.id+".")
        
    def create(self):
        try:
            saver.data[saver.selected_save][self.type][self.id] = {}
            self.load()
        except:
            warn("Can't create object of type "+self.type+" with id "+self.id+".")

    def get(self, parameter:str):
        return saver.data[saver.selected_save][self.type][self.id][parameter]
    
    def set(self, parameter:str, value:any):
        saver.data[saver.selected_save][self.type][self.id][parameter] = value