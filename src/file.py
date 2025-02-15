import json, pygame, os, copy, error

class path:
    bin:str = "../bin/"
    playground:str = "../test/playground/"
    tilemap:str = "../resources/tilemaps/"
    background:str = "../resources/backgrounds/"

class ext:
    data:str = ".json"
    text:str = ".txt"
    image:str = ".png"
    log:str = ".log"

files = {}
    
def create(path:str, data=None) -> None:
    files[f"{path}"] = data

def close(path:str) -> None|error.Error:
    try:
        del files[f"{path}"]
    except KeyError:
        return error.Error(error.group.already_done, f"The variable '{path}' is already deleted")
               
def duplicate(old_path:str, new_path:str) -> None|error.Error:
    if f"{old_path}" not in files:
        return error.Error(error.group.not_found, f"Can't find the file '{old_path}' in memory")
    
    if old_path.endswith(ext.image) == True:
        files[f"{new_path}"] = files[f"{old_path}"].copy()
    else:
        files[f"{new_path}"] = copy.deepcopy(files[f"{old_path}"])

def read(path:str) -> None|error.Error:
    try:
        match "."+path.split(".")[-1]:
            case ext.data:
                files[f"{path}"] = json.load(open(f"{path}", "r"))
            case ext.image:
                files[f"{path}"] = pygame.image.load(f"{path}").convert_alpha()
            case ext.text|ext.log:
                files[f"{path}"] = open(f"{path}", "r").read()
            case _:
                return error.Error(error.group.unsupported,f"Can't open, unknown extension '{"."+path.split(".")[-1]}'")
            
    except FileNotFoundError:
        return error.Error(error.group.not_found, f"File {path} not found")

    except pygame.error:
        return error.Error(error.group.pygame_uninitialize, f"Can't open image '{path}' without initializing pygame")

def delete(path:str) -> None|error.Error:
    try:
        os.remove(f"{path}")
    except FileNotFoundError:
        return error.Error(error.group.not_found, f"The file '{path}' is already deleted")
        
def write(path:str) -> None|error.Error:
    if path not in files:
        return error.Error(error.group.not_found, f"The file '{path}' is not in memory")
    match "."+path.split(".")[-1]:
        case ext.data:
            json.dump(files[f"{path}"], open(f"{path}", "w"), indent=4)
        case ext.image:
            pygame.image.save(files[f"{path}"], f"{path}")
        case ext.text|ext.log:
            open(f"{path}", "w").write(files[f"{path}"])
        case _:
            return error.Error(error.group.unsupported, f"Can't write, unknown extension '{"."+path.split(".")[-1]}'")
        
def ask(path:str) -> object|error.Error:
    if path not in files:
        err = read(path)
    return files.get(path, err)

def directory(path:str) -> None|error.Error:
    try:
        os.makedirs(f"{path}")
    except OSError:
        return error.Error(error.group.already_done, f"The directory '{path}' already exist")

def find(path:str) -> bool:
    return os.path.exists(f"{path}")