# This is a tool box that gives functions to manipulate files.
#
# FUNCTION:
#  - shortset: manipulate shortcuts creation, renaming, destuction, etc.
#  - addressof: get the adress of a file by passing its shortcut, name(with extension) or the default file.
#
#  - file_read: read a file (json, txt) and return its content.
#  - file_create: create a new file (json, txt) and return True if the operation has been done.
#  - file_delete: delete a file (json, txt) and return True if the operation has been done.
#  - file_rename: rename a file (json, txt) and return True if the operation has been done.
#
#  - param_get: get a parameter from a json file and return its value.
#  - param_getlist: get multiple parameters from a json file and yield their values.
#  - param_set: set multiple parameters in a json file and return True if the operation has been done.
#  - param_del: delete multiple parameters in a json file and return True if the operation has been done.
#  - param_reset: reset/patternate a json file and return True if the operation has been done.
import json
import os
from utils.consoleHandler import error, warn, debug, trace, info

# Fast functions (function that use the storage class to be used elsewere)
def file_read(file_name:str=None, type=None): return storage.file_read(file_name, type)
def file_create(file_name:str, type=None, content=None, short:str=None): return storage.file_create(file_name, type, content, short)
def file_delete(file_name:str, type=None): return storage.file_delete(file_name, type)
def file_rename(file_name:str, new_name:str, type=None): return storage.file_rename(file_name, new_name, type)
def param_get(param_name:str, file_name:str=None): return storage.parameter_get(param_name, file_name)
def param_getlist(param_name, file_name=None):
    """Get  a list of parameters"""
    if type(param_name) != list:
        warn("param_getlist take param_name as a list. No other types allowed.")
        yield None
    if type(file_name) == str:
        file_name = [file_name]*len(param_name)
    elif file_name == None:
        file_name = [None]*len(param_name)
    elif type(file_name) != list:
        warn("param_getlist take file_name as a list or str. No other types allowed.")
        yield None
    for k in range(len(param_name)):
        yield storage.parameter_get(param_name[k], file_name[k])
def param_set(param_name:str, param_value:str, file_name:str=None): return storage.parameter_set(param_name, param_value, file_name)
def param_del(param_name:str, file_name:str=None): return storage.parameter_delete(param_name, file_name)
def param_reset(file_name:str=None, reset:dict={}): return storage.parameter_reset(file_name, reset)
    

class storageHandler():

    def __init__(self):
        # Setting up the storage handler
        if self.set_storage_folder_path("assets/storage/") == False:
            warn("Storage folder path not found!")
        if self.set_shortcuts_file_path("shortcuts.json") == False:
            warn("Shortcuts file not found!")

        info("Storage handler initialized")

    def quit(self):
        """Save the shortcuts and quit"""
        self.parameter_reset("shortcuts", self.shortcuts)
        info("Storage handler has quit")

    def set_storage_folder_path(self, folder_path:str):
        """
        Set the storage folder path.

        Args:
            path (str): path to the folder where the files are.

        Returns:
            True if the path has been set. False otherwise.
        """
        if os.path.isdir(folder_path):
            self.storage_folder_path = folder_path
            return True
        else:
            self.storage_folder_path = None
            return False
        
    def set_shortcuts_file_path(self, file_path:str):
        """
        Set the shortcuts file.

        Args:
            file_path (str): path to the shortcuts file.

        Returns:
            True if the path has been set. False otherwise.
        """
        if os.path.isfile(self.storage_folder_path+file_path):
            self.shortcuts = self.file_read(file_path)
            return True
        else:
            self.shortcuts = None
            return False

    def set_shortcut(self, new_file_name:str=None, old_file_name:str=None, new_file_short:str=None, old_file_short:str=None):
        """
        Set a shortcut.

        Args:
            new_file_name (str): name of the new file.
            old_file_name (str): name of the old file.
            new_file_short (str): shortcut of the new file.
            old_file_short (str): shortcut of the old file.


        Returns:
            True if the shortcut has been set. False otherwise.
        """
        # Set new file name if not set.
        if new_file_name != None and new_file_short == None:
            new_file_short, type = new_file_name.split(".", 1)
            type = "."+type
        elif new_file_name != None:
            type = new_file_name.split(".", 1)[-1]
            type = "."+type

        # Set old file name if not set.
        if old_file_name != None and old_file_short == None:
            old_file_short, old_type = old_file_name.split(".", 1)
            old_type = "."+old_type
        elif old_file_name != None:
            old_type = old_file_name.split(".", 1)[-1]
            old_type = "."+old_type

        # Rename a shortcut.
        if old_file_name != None and new_file_name != None:
            if old_file_name in self.shortcuts.values():
                for key in self.shortcuts.keys():
                    if self.shortcuts[key] == old_file_name:
                        break
                del self.shortcuts[key]
            if not new_file_short in self.shortcuts.keys():
                self.shortcuts[new_file_short] = new_file_name
            else:
                warn("Shortcut already exists. Can't apply new shortcut.")
                return False
        # Set a new shortcut.
        elif new_file_name != None and old_file_name == None:
            if not new_file_short in self.shortcuts.keys():
                self.shortcuts[new_file_short] = new_file_name
            else:
                warn("Shortcut already exists. Can't apply new shortcut.")
                return False
        # Delete a shortcut.
        elif new_file_name == None and old_file_name != None:
            if old_file_name in self.shortcuts.values():
                for key in self.shortcuts.keys():
                    if self.shortcuts[key] == old_file_name:
                        break
                del self.shortcuts[key]
        # No input.
        else :
            warn("Wrong input command.")
            return False
        return True

    def get_address_of(self, file_name:str):
        """
        Get the adress of a file by passing its shortcut, name(with extension) or the default file is not set.

        Args:
            file_name (str): name of the file.

        Returns:
            The adress of the file (str). None if the file doesn't exist.
        """
        if file_name is None or file_name == "":
            file_name = self.shortcuts["default"]
        elif file_name.count(".json") == 0:
            if file_name in self.shortcuts.keys():
                file_name = self.shortcuts[file_name]
            else:
                warn("Unknown file name.")
                return None
        if os.path.exists(self.storage_folder_path + file_name):
            return file_name
        else:
            warn("Unknown file "+file_name+". Make sure the file exists.")
            return None


    ##################
    # FILE FUNCTIONS #
    ##################
    def file_read(self, file_name:str=None, type=None):
        """
        Read a file and return its content.

        Args:
            file_name (str): name of the file.

        Returns:
            The content of the file (str).
        """
        file_name = self.get_address_of(file_name)
        if file_name is None:
            error("No files can be read!")
            return None
        if type is None:
            file_name, temp = file_name.split(".", 1)
            type = "."+temp
        if os.path.exists(self.storage_folder_path+file_name+type):
            with open(self.storage_folder_path+file_name+type) as file:
                if type == ".json":
                    return json.load(file)
                elif type == ".txt":
                    return file.read()
                warn("Unknown file type.")
                return None
        else:
            warn("No files were found")
            return None
            
    def file_create(self, file_name:str, type=None, content=None, short:str=None):
        """
        Create a new file.

        Args:
            file_name (str): name of the file.
            type (str): type of the file.
            content: content of the file.
            short (str): shortcut of the file.

        Returns:
            None
        """
        if type is None:
            file_name, temp = file_name.split(".", 1)
            type = "."+temp
        if os.path.exists(self.storage_folder_path+file_name+type):
            self.file_delete(file_name, type)
        with open(self.storage_folder_path+file_name+type, "a") as file:
            if type == ".json":
                if content != None:
                    json.dump(content, file, indent=4)
                else:
                    file.write("{\n\n}")
                self.set_shortcut(file_name+type, None, short)
                return True
            elif type == ".txt":
                if content != None:
                    file.write(content)
                self.set_shortcut(file_name+type, None, short)
                return True
            warn("Unknown file type.")
            return False
            
    def file_delete(self, file_name:str, type:str=None):
        """
        Delete a file.

        Args:
            file_name (str): name of the file.

        Returns:
            None
        """
        if type is None:
            file_name = self.get_address_of(file_name)
            if file_name is None:
                warn("No file has been deleted.")
                return False
            file_name, temp = file_name.split(".", 1)
            type = "."+temp
        if not os.path.exists(self.storage_folder_path+file_name+type):
            warn("Unknown file.")
            return False
        os.remove(self.storage_folder_path+file_name+type)
        self.set_shortcut(None, file_name+type)
        if os.path.exists(self.storage_folder_path+file_name+type):
            error("Unable to delete.")
            return False
        return True
        
    def file_rename(self, old_name:str, new_name:str, short:str=None):
        """
        Get a file and rename it and also his shortcut

        Args:
            old_name (str): old name of the file or shortcut.
            new_name (str): new name of the file.
            short (str): new name of the shortcut.

        Return:

        """
        old_name = self.get_address_of(old_name)
        old_name, type = old_name.split(".", 1)
        new_name = new_name.split(".", 1)[0]
        type = "."+type
        if short == None:
            short = new_name
        
        if old_name == None:
            warn("File can't be rename because unable to open")
            return False
        if os.path.exists(self.storage_folder_path+new_name+type) == True:
            debug("Rename has replaced the same named file.")
            self.file_delete(new_name, type)
        os.rename(self.storage_folder_path+old_name+type, self.storage_folder_path+new_name+type)
        self.set_shortcut(new_name+type, old_name+type, short)
        return True


    ###################
    # PARAM FUNCTIONS #
    ###################
    def parameter_get(self, param_name:str, file_name:str=None):
        """
        Get a parameter from a file.

        Args:
            param_name (str): name of the parameter.
            file_name (str): name of the file.

        Returns:
            The value of the parameter (str).
        """
        # Verify if the file exists in all the shortcuts files.
        if file_name == None:
            for file in self.shortcuts:
                if param_name in self.file_read(self.shortcuts[file]):
                    file_name = self.shortcuts[file]
                    break

        # Set the file address
        file_name = self.get_address_of(file_name)
        if file_name is None:
            warn("No files can be read!")
            return None
        
        if type(param_name) != str:
            warn("param_get take param_name as a str. No other types allowed.")
            return False
        if param_name in self.file_read(file_name):
            return self.file_read(file_name)[param_name]
        warn("Unknown parameter.")
        return None
        
    def parameter_set(self, param_name, param_value, file_name=None):
        """
        Set multiple parameters in a file.

        Args:
            param_name (list): name of the parameter.
            param_value (list): value of the parameter.
            file_name (list): name of the file.

        Returns:
            True if all the parameters have been set. False otherwise.
        """
        if type(param_name) == str:
            param_name = [param_name]
            param_value = [param_value]
        elif type(param_name) != list or type(param_value) != list:
            warn("param_setlist take parameters as a list or str. No other types allowed.")
            return False
        if file_name == None:
            file_name = [""]*len(param_name)
        elif type(file_name) == str:
            file_name = [file_name]*len(param_name)
        for k in range(len(param_name)):
            file_name[k] = self.get_address_of(file_name[k])

            if file_name[k] is None:
                warn("No files can be read!")
                return False
            modified = self.file_read(file_name[k])
            modified[param_name[k]] = param_value[k]
            json.dump(modified, open(self.storage_folder_path+file_name[k], "w"), indent=4)
        return True

    def parameter_delete(self, param_name, file_name=None):
        """
        Delete multiple parameters in a file.

        Args:
            param_name (list): name of the parameter.
            file_name (str): name of the file.

        Returns:
            True if all the parameters have been deleted. False otherwise.
        """
        if type(param_name) == str:
            param_name = [param_name]
        elif type(param_name) != list:
                warn("param_dellist take param_name as a list. No other types allowed.")
                return False
        if file_name is None:
            warn("No files can be deleted!")
            return False
        elif type(file_name) == str:
            file_name = [file_name]*len(param_name)
        
        for k in range(len(param_name)):
            file_name[k] = self.get_address_of(file_name[k])
        
            if param_name[k] in self.file_read(file_name[k]).keys():
                modified = self.file_read(file_name[k])
                del modified[param_name[k]]
                json.dump(modified, open(self.storage_folder_path+file_name[k], "w"), indent=4)
            else:
                trace("There is no parameter with this name. Skip.")
                return False
        return True  

    def parameter_reset(self, file_name:str=None, reset:dict={}):
        """
        Reset a parameter in a file.

        Args:
            file_name (str): name of the file.

        Returns:
            True if the file has been reset. False otherwise.
        """
        file_name = self.get_address_of(file_name)
        if file_name is None:
            warn("No files can be read!")
            return False
        
        json.dump(reset, open(self.storage_folder_path+file_name, "w"), indent=4)
        return True

# Set the storage object
storage = storageHandler()