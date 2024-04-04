# This file serve the purpose of reading a file and reporting options and variables
import json
import os
from logger import *
json_folder_path = "storage/"
shortcuts = {}


def addressof(file_name:str):
    """
    Get the adress of a file. (it's used for shortcuts)

    Args:
        file_name (str): name of the file.

    Returns:
        The adress of the file (str).
    """
    global shortcuts
    if file_name is None:
        file_name = shortcuts["default"]
    elif file_name.count(".json") == 0:
        if file_name in shortcuts:
            file_name = shortcuts[file_name]
        else:
            WARN("Unknown file name.")
            return None
    if os.path.exists(json_folder_path + file_name):
        return file_name
    else:
        WARN("Unknown file "+file_name+". Make sure the file exists.")
        return None 

##################
# FILE FUNCTIONS #
##################
def file_read(file_name=None, type=None):
    """
    Read a file and return its content.

    Args:
        file_name (str): name of the file.

    Returns:
        The content of the file (str).
    """
    file_name = addressof(file_name)
    if file_name is None:
        ERROR("No files can be read!")
        return None
    if type is None:
        file_name, temp = file_name.split(".", 1)
        type = "."+temp
    if os.path.exists(json_folder_path+file_name+type):
        with open(json_folder_path+file_name+type) as file:
            if type == ".json":
                return json.load(file)
            elif type == ".txt":
                return file.read()
            WARN("Unknown file type.")
            return None
    else:
        ERROR("No files were found")
        return None
        
def file_create(file_name:str, type=None, content:str=None):
    """
    Create a new file.

    Args:
        file_name (str): name of the file.

    Returns:
        None
    """
    if type is None:
        file_name, temp = file_name.split(".", 1)
        type = "."+temp
    if os.path.exists(json_folder_path+file_name+type):
        file_delete(file_name, type)
    with open(json_folder_path+file_name+type, "a") as file:
        if type == ".json":
            if content != "None":
                file.write("{\n"+content+"\n}")
            else:
                file.write("{}")
            shortcuts[file_name] = json_folder_path+file_name+type
            return True
        elif type == ".txt":
            if content != "None":
                file.write(content)
            return True
        WARN("Unknown file type.")
        return False
        
def file_delete(file_name, type):
    """
    Delete a file.

    Args:
        file_name (str): name of the file.

    Returns:
        None
    """
    if type is None:
        file_name, temp = file_name.split(".", 1)
        type = "."+temp
    os.remove(json_folder_path+file_name+type)
    if file_name in shortcuts:
        del shortcuts[file_name]
        return True
    WARN("Unknown file. Unable to delete.")
    return(False)
    

def file_rename(filename:str, new_name:str, shortcut:str=None):
   """
   Get a file and rename it and also his shortcut

   Args:

   Return:

   """
   filename = addressof(filename)
   if filename == None:
      WARN("File can't be rename because unable to open")
      return(False)

###################
# PARAM FUNCTIONS #
###################
def param_get(param_name:str, file_name:str=None):
    """
    Get a parameter from a file.

    Args:
        param_name (str): name of the parameter.
        file_name (str): name of the file.

    Returns:
        The value of the parameter (str).
    """
    if file_name == None:
        for file in shortcuts:
            if param_name in file_read(shortcuts[file]):
                file_name = shortcuts[file]
                break
    file_name = addressof(file_name)
    if file_name is None:
        WARN("No files can be read!")
        return None
    
    if type(param_name) != str:
        WARN("param_get take param_name as a str. No other types allowed.")
        return(False)
    if param_name in file_read(file_name):
        return file_read(file_name)[param_name]
    WARN("Unknown parameter.")
    return None
    
def param_getlist(param_name:str, file_name:str=None):
    """
    Get a parameter from a file.

    Args:
        param_name (list): name of the parameter.
        file_name (list): name of the file.

    Returns:
        The value of the parameter (list).
    """
    if file_name is None:
        for file in shortcuts:
            if param_name in file_read(shortcuts[file]):
                file_name = shortcuts[file]
                break
    
    file_name = addressof(file_name)
    if file_name is None:
        WARN("No files can be read!")
        return None
    
    list = []
    if type(param_name) != list:
        WARN("param_getlist take param_name as a list. No other types allowed.")
        return(None)
    for k in range(len(param_name)):
        if param_name[k] in file_read(file_name):
            list.append(file_read(file_name)[param_name[k]])
        else:
            TRACE("Unknown element in the list.")
            list.append(None)
    return list
    
def param_set(param_name:str, param_value, file_name:str=None):
    """
    Set a parameter in a file.

    Args:
        param_name (str): name of the parameter.
        param_value : value of the parameter.
        file_name (str): name of the file.

    Returns:
        None
    """
    file_name = addressof(file_name)
    if file_name is None:
        WARN("No files can be read!")
        return(False)

    if type(param_name) != str:
        WARN("param_set take param_name as a str. No other types allowed.")
        return(False)
    modified = file_read(file_name)
    modified[param_name] = param_value
    json.dump(modified, open(file_name, "w"))
    return(True)
    
def param_setlist(param_name:list, param_value:list, file_name:str=None):
    """
    Set a parameter in a file.

    Args:
        param_name (list): name of the parameter.
        param_value (list): value of the parameter.
        file_name (list): name of the file.

    Returns:
        None
    """
    if type(param_name) != list:
        WARN("param_setlist take param_name as a list. No other types allowed.")
        return(False)
    file_name = addressof(file_name)

    if file_name is None:
        WARN("No files can be read!")
        return(False)
    modified = file_read(file_name)
    for k in range(len(param_name)):
        modified[param_name[k]] = param_value[k]
    json.dump(modified, open(file_name, "w"))
    return(True)

def param_del(param_name:str, file_name:str=None):
    """
    Delete a parameter in a file.

    Args:
        param_name (str): name of the parameter.
        file_name (str): name of the file.

    Returns:
        None
    """
    file_name = addressof(file_name)
    if file_name is None:
        WARN("No files can be read!")
        return(False)
    
    if type(param_name) != str:
        WARN("param_del take param_name as a str. No other types allowed.")
        return(False)
    if not param_name in file_read(file_name).keys():
        WARN("There is no parameter with this name. Nothing to delete.")
        return(False)
    modified = file_read(file_name)
    del modified[param_name]
    json.dump(modified, open(file_name, "w"))
    return(True)

def param_dellist(param_name:list, file_name:str=None):
    """
    Delete a parameter in a file.

    Args:
        param_name (list): name of the parameter.
        file_name (str): name of the file.

    Returns:
        None
    """
    file_name = addressof(file_name)
    if file_name is None:
        WARN("No files can be read!")
        return(False)
    
    if type(param_name) != list:
        WARN("param_dellist take param_name as a list. No other types allowed.")
        return(False)
    for k in range(len(param_name)):
        if param_name[k] in file_read(file_name).keys():
            modified = file_read(file_name)
            del modified[param_name[k]]
            json.dump(modified, open(file_name, "w"))
        else:
            TRACE("There is no parameter with this name. Skip.")
            return(False)
    return(True)  

def param_reset(file_name:str=None, reset:dict={}):
    """
    Reset a parameter in a file.

    Args:
        file_name (str): name of the file.

    Returns:
        None
    """
    file_name = addressof(file_name)
    if file_name is None:
        WARN("No files can be read!")
        return(False)
    
    json.dump(reset, open(file_name, "w"))
    return(True)

#Set shortcuts
shortcuts = file_read("shortcuts.json")