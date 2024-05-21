from utils.consoleSystem import error, warn, info, trace, exception
import json
import os

class resourcesHandler():

    def __init__(self, name:str, default:str=None):
        # Setting up the storage handler
        self.handler_name:str = name
        self.handler_default:str = default
        self.handler_folder:str = "resources/"+self.handler_name+"/"
        self.loaded:dict = {}
        try:
            self.paths = json.load(open("resources/"+self.handler_name+".json", "r"))
            info(self.handler_name.capitalize()+" handler initialized.")
        except Exception as e:
            error(self.handler_name.capitalize()+" handler can't be initialized.")
            exception(e)


    def quit(self):
        """Save the file_names and quit"""
        try:
            for file_name in self.loaded:
                self.unload_file(file_name)
            json.dump(self.paths, open("resources/"+self.handler_name+".json", "w"), indent=4)
            info(self.handler_name.capitalize()+" handler has quit.")
        except Exception as e:
            warn("Can't quit "+self.handler_name.capitalize()+" handler.")
            exception(e)

    ###############
    # File system #
    ###############
    def load_file(self, file_name:str):
        """
        Read a file and append it to the loaded dict.
        """
        file_path = self.paths[file_name]["path"]
        file_type = self.paths[file_name]["type"]
        try:
            match file_type:
                case "json":
                    self.loaded[file_name] = {"data":json.load(open(self.handler_folder+file_path, "r")), "path":file_path, "type":file_type}
                case "txt":
                    self.loaded[file_name] = {"data":open(self.handler_folder+file_path, "r").read(), "path":file_path, "type":file_type}
                case _:
                    self.loaded[file_name] = None
                    warn("File type '"+str(file_type)+"' not recognized.")
                    return False
            trace("File '"+str(file_name)+"' loaded.")
            return True
        except Exception as e:
            self.loaded[file_name] = None
            warn("Can't load file '"+str(file_name)+"'.")
            exception(e)
            return False

    def unload_file(self, file_name:str):
        """
        Write a file with his loaded counterpart.
        """
        try:
            file_path = self.paths[file_name]["path"]
            file_type = self.paths[file_name]["type"]
            match file_type:
                case "json":
                    json.dump(self.loaded[file_name]["data"], open(self.handler_folder+file_path, "w"), indent=4)
                case "txt":
                    open(self.handler_folder+file_path, "w").write(self.loaded[file_name]["data"])
                case _:
                    warn("File type '"+str(file_type)+"' not recognized.")
                    return False
            trace("File '"+str(file_name)+"' unloaded.")
            return True
        except Exception as e:
            warn("Can't unload file '"+str(file_name)+"'.")
            exception(e)
            return False

    
    def read_file(self, file_name:str):
        """
        Return the content of a file in the loaded dict. If he doesn't exist, load it and retry.
        """
        try:
            if not file_name in self.loaded:
                self.load_file(file_name)
            return self.loaded[file_name]["data"]
        except Exception as e:
            warn("Can't read file '"+str(file_name)+"'.")
            exception(e)
            return None

    def write_file(self, file_name:str, data):
        """
        Rewrite the loaded file with the data given. If he doesn't exist, load it and retry.
        """
        try:
            if not file_name in self.loaded:
                self.load_file(file_name)
            self.loaded[file_name]["data"] = data
            return True
        except Exception as e:
            warn("Can't write file '"+str(file_name)+"'.")
            exception(e)
            return False

    def line_file(self, file_name:str, data):
        """
        Append a line to the loaded file (only for txt files).
        """
        try:
            if not file_name in self.loaded:
                self.load_file(file_name)
            if self.loaded[file_name]["type"] == "txt":
                self.loaded[file_name]["data"] += "\n"+str(data)
                return True
            raise Exception("The function line_file() can only be used for txt files.")
        except Exception as e:
            warn("Can't add a line to '"+str(file_name)+"'.")
            exception(e)
            return False

    def create_file(self, file_name:str, file_type:str):
        """
        Create load a new file. Write on disk on unload.
        """
        try:
            match file_type:
                case "json":
                    self.paths[file_name] = {"path":file_name+"."+file_type, "name":file_name, "type":file_type}
                    self.loaded[file_name] = {"data":{}, "path":file_name+file_type, "type":file_type}
                case "txt":
                    self.paths[file_name] = {"path":file_name+"."+file_type, "name":file_name, "type":file_type}
                    self.loaded[file_name] = {"data":"", "path":file_name+file_type, "type":file_type}
                case _:
                    warn("File type '"+str(file_type)+"' not recognized.")
                    return False
            trace("File '"+str(file_name)+"' created.")
            return True
        except Exception as e:
            warn("Can't create file '"+str(file_name)+"'.")
            exception(e)
            return False
        
    def delete_file(self, file_name:str):
        """
        Delete the file.
        """
        try:
            if file_name in self.loaded:
                del self.loaded[file_name]
            os.remove(self.handler_folder+file_name+"."+self.paths[file_name]["type"])
            del self.paths[file_name]
            trace("File '"+str(file_name)+"' deleted.")
            return True
        except Exception as e:
            warn("Can't delete file '"+str(file_name)+"'.")
            exception(e)
            return False
            

    def rename_file(self, old_name:str, new_name:str):
        """
        Rename a file and rename the key in the loaded dict.
        """
        try:
            if old_name in self.loaded:
                self.loaded[new_name] = self.loaded[old_name]
                del self.loaded[old_name]
            os.remove(self.handler_folder+old_name+"."+self.paths[old_name]["type"])
            self.create_file(new_name, self.paths[old_name]["type"])
            self.paths[new_name] = self.paths[old_name]
            del self.paths[old_name]
            trace("File '"+str(old_name)+"' renamed to '"+str(new_name)+"'.")
            return True
        except Exception as e:
            warn("Can't rename file '"+str(old_name)+"'.")
            exception(e)
            return False 

    #############
    # JSON part #
    #############
    def get(self, parameter:str|list[str], loaded_file_name:str=None):
        """
        Return a parameter from a file in the loaded dict. If he doesn't exist, load it and retry.
        """
        if loaded_file_name == None:
            loaded_file_name = self.handler_default
        try:
            if not loaded_file_name in self.loaded:
                self.load_file(loaded_file_name)
            if type(parameter) == list:
                return [self.loaded[loaded_file_name]["data"][key] for key in parameter]
            return self.loaded[loaded_file_name]["data"][parameter]
        except Exception as e:
            warn("Can't get parameter '"+str(parameter)+"' from file '"+str(loaded_file_name)+"'.")
            exception(e)
            return None

    def set(self, parameter:str|list[str], value:any, loaded_file_name:str=None):
        """
        Set the parameter in the file of the loaded dict. If he doesn't exist, load it and retry.
        """
        if loaded_file_name == None:
            loaded_file_name = self.handler_default
        try:
            if not loaded_file_name in self.loaded:
                self.load_file(loaded_file_name)
            if type(parameter) == list and type(value) == list:
                for index in range(parameter):
                    self.loaded[loaded_file_name]["data"][parameter[index]] = value[index]
            else:
                self.loaded[loaded_file_name]["data"][parameter] = value
            return True
        except Exception as e:
            warn("Can't set parameter '"+str(parameter)+"' in file '"+str(loaded_file_name)+"'.")
            exception(e)
            return False

    def cut(self, parameter:str|list[str], loaded_file_name:str):
        """
        Delete the parameter in the file of the loaded dict. If he doesn't exist, load it and retry.
        """
        try:
            if not loaded_file_name in self.loaded:
                self.load_file(loaded_file_name)
            if type(parameter) == list:
                for key in parameter:
                    del self.loaded[loaded_file_name]["data"][key]
            else:
                del self.loaded[loaded_file_name]["data"][parameter]
            return True
        except Exception as e:
            warn("Can't cut parameter '"+str(parameter)+"' in file '"+str(loaded_file_name)+"'.")
            exception(e)
            return False

# Set the storage object
storage = resourcesHandler("storage", "options")
save = resourcesHandler("save", "options")