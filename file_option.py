# This file serve the purpose of reading a file and reporting options and variables
import json
import os

def read_file(file_name):
    with open(file_name) as file:
        if file_name.endswith(".json"):
            return json.load(file)
        elif file_name.endswith(".txt"):
            return file.read()
        else:
            return None

def txt_to_dict(file):
    """
    Convert txt file to dict

    Args:
        file (txt file): txt file to be converted to dict

    Returns:
        dict: dict of the txt file with the key and value separed by a ':'
    """
    dict = {}
    key = ""
    value = ""
    type = ""
    now = ""
    next = file
    for line in range(file.count('\n')+1):
        now, next = next.split('\n')
        if now != '':
            key, value = now.split(':')
            value, type = value.split(' ')
            if type == 'int':
                value = int(value)
            elif type == 'float':
                value = float(value)
            elif type == 'str':
                value = str(value)
            elif type == 'bool':
                value = bool(value)
            else:
                return None
            dict = {key: value}
    return dict

def load_parameters(para_name:str, file_name:str="game_option"):
    """
    Load all option files (txt and json) and try to find the key corresponding to the parameter

    Args:
        para_name (str): name of the txt file

    Returns:
        The value of the parameter (int, float, str, bool)
    """
    
    if os.path.isfile(file_name+".json") and para_name in json.load(read_file(file_name+".json")):
        return json.load(open(file_name+".json", 'r'))[para_name]
    if os.path.isfile(file_name+".txt") and para_name in txt_to_dict(read_file(file_name+".txt")):
        return txt_to_dict(open(file_name+".txt", 'r').read())[para_name]
    return None

print(load_parameters("lui"))