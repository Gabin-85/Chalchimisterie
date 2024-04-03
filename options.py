import json

def getJson(file_name):
    with open(file_name) as file:
        return json.load(file)
    