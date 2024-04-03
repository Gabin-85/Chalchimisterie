# This file serve the purpose of reading a file and reporting options and variables
import json
import os
shortcuts = {}

def addressof(file_name:str):
    """
    Get the adress of a file. (it's for using shortcuts)

    Args:
        file_name (str): name of the file.

    Returns:
        The adress of the file (str).
    """
    global shortcuts
    if file_name is None:
        file_name = shortcuts["default"]
    elif file_name.count(".json") == 0:
        file_name = shortcuts[file_name]
    return file_name

##################
# FILE FUNCTIONS #
##################
def file_read(file_name:None, type=None):
    """
    Read a file and return its content.

    Args:
        file_name (str): name of the file.

    Returns:
        The content of the file (str).
    """
    file_name = addressof(file_name)
    if type is None:
        file_name, temp = file_name.split(".", 1)
        type = "."+temp
    if os.path.exists(file_name+type):
        with open(file_name+type) as file:
            if type == ".json":
                return json.load(file)
            elif type == ".txt":
                return file.read()
            else:
                return None
        
def file_create(file_name:str, type=None, content:str="None"):
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
    if os.path.exists(file_name+type):
        file_delete(file_name, type)
    with open(file_name+type, "a") as file:
        if type == ".json":
            if content != "None":
                file.write("{\n"+content+"\n}")
            else:
                file.write("{}")
            shortcuts[file_name] = file_name+type
            return True
        elif type == ".txt":
            if content != "None":
                file.write(content)
            return True
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
    os.remove(file_name+type)
    if file_name in shortcuts:
        del shortcuts[file_name]


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
    if file_name is None:
        for file in shortcuts:
            if param_name in file_read(shortcuts[file]):
                file_name = shortcuts[file]
                break
    file_name = addressof(file_name)
    if param_name in file_read(file_name):
        return file_read(file_name)[param_name]
    else:
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
    list = []
    for k in range(len(param_name)):
        if param_name[k] in file_read(file_name):
            list.append(file_read(file_name)[param_name[k]])
        else:
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
    if type(param_name) == list:
        return(False)
    file_name = addressof(file_name)
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
    if type(param_name) == list:
        return(False)
    file_name = addressof(file_name)
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
    if not param_name in file_read(file_name).keys():
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
    for k in range(len(param_name)):
        if param_name[k] in file_read(file_name).keys():
            modified = file_read(file_name)
            del modified[param_name[k]]
            json.dump(modified, open(file_name, "w"))
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
    json.dump(reset, open(file_name, "w"))
    return(True)

# Set live shortcuts to shortcuts template
shortcuts = file_read("shortcuts.json")