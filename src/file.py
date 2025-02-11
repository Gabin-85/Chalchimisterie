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
    
def create(paths:list[str], data=None) -> None:
    for path in paths:
        files[f"{path}"] = data

def close(paths:list[str]) -> list[error.Error]:
    err = []
    for path in paths:
        try:
            del files[f"{path}"]
        except KeyError:
            err.append(error.Error(error.category.already_done, f"The variable '{path}' is already deleted"))
    return err
               
def duplicate(old_path:str, new_paths:list[str]) -> None|error.Error:
    if f"{old_path}" not in files:
        return error.Error(error.category.not_found, f"Can't find the file '{old_path}' in memory")
    
    for new_path in new_paths:
        if old_path.endswith(ext.image) == True:
            files[f"{new_path}"] = files[f"{old_path}"].copy()
        else:
            files[f"{new_path}"] = copy.deepcopy(files[f"{old_path}"])

def read(paths:list[str]) -> list[error.Error]:
    err = []
    for path in paths:
        try:
            match "."+path.split(".")[-1]:
                case ext.data:
                    files[f"{path}"] = json.load(open(f"{path}", "r"))
                case ext.image:
                    files[f"{path}"] = pygame.image.load(f"{path}").convert_alpha()
                case ext.text|ext.log:
                    files[f"{path}"] = open(f"{path}", "r").read()
                case _:
                    err.append(error.Error(error.category.unsupported,f"Can't open, unknown extension '{"."+path.split(".")[-1]}'"))
            
        except FileNotFoundError:
            err.append(error.Error(error.category.not_found, f"File {path} not found"))

        except pygame.error:
            err.append(error.Error(error.category.pygame_uninitialize, f"Can't open image '{path}' without initializing pygame"))
    return err

def delete(paths:list[str]) -> list[error.Error]:
    err = []
    for path in paths:
        try:
            os.remove(f"{path}")
        except FileNotFoundError:
            err.append(error.Error(error.category.not_found, f"The file '{path}' is already deleted"))
    return err
        
def write(paths:list[str]) -> list[error.Error]:
    err = []
    for path in paths:
        if path not in files:
            err.append(error.Error(error.category.not_found, f"The file '{path}' is not in memory"))
            continue
        match "."+path.split(".")[-1]:
            case ext.data:
                json.dump(files[f"{path}"], open(f"{path}", "w"), indent=4)
            case ext.image:
                pygame.image.save(files[f"{path}"], f"{path}")
            case ext.text|ext.log:
                open(f"{path}", "w").write(files[f"{path}"])
            case _:
                err.append(error.Error(error.category.unsupported, f"Can't write, unknown extension '{"."+path.split(".")[-1]}'"))
    return err

def ask(paths:list[str]) -> list[object|error.Error]:
    read([path for path in paths if path not in files])
    return [files.get(path, error.Error(error.category.not_found, f"File {path} not found")) for path in paths]

def directory(paths:list[str]) -> list[error.Error]:
    err = []
    for path in paths:
        try:
            os.makedirs(f"{path}")
        except OSError:
            err.append(error.Error(error.category.already_done, f"The directory '{path}' already exist"))
    return err

def find(paths:list[str]) -> list[bool]:
    result = []
    for path in paths:
        result.append(os.path.exists(f"{path}"))
    return result