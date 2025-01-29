import json, pygame, os, copy, console
from args import ext

files = {}
    
def create(paths:list[str], data=None) -> None:
    for path in paths:
        files[f"{path}"] = data

def close(paths:list[str]) -> None:
    for path in paths:
        try:
            del files[f"{path}"]
        except KeyError:
            pass
    
def duplicate(old_path:str, new_paths:list[str]) -> None:
    if f"{old_path}" not in files:
        console.warn(f"Can't find the file '{old_path}' in memory.")
        return
    
    for new_path in new_paths:
        files[f"{new_path}"] = copy.deepcopy(files[f"{old_path}"])

def read(paths:list[str]) -> None:
    for path in paths:
        try:
            match "."+path.split(".")[-1]:
                case ext.data:
                    files[f"{path}"] = json.load(open(f"{path}", "r"))
                case ext.image:
                    files[f"{path}"] = pygame.image.load(f"{path}").convert_alpha()
                case ext.text:
                    files[f"{path}"] = open(f"{path}", "r").read()
                case _:
                    console.warn(f"Can't open, unknown extension '{"."+path.split(".")[-1]}'.")
            
        except FileNotFoundError:
            console.warn(f"File {path} not found.")

        except pygame.error as err:
            if err.args[0] != "cannot convert without pygame.display initialized":
                raise(err)
            console.error(f"Can't open image '{path}' without initializing pygame")
            

def delete(paths:list[str]) -> None:
    for path in paths:
        try:
            os.remove(f"{path}")
        except FileNotFoundError:
            pass


def write(paths:list[str]) -> None:
    for path in paths:
        try:
            match "."+path.split(".")[-1]:
                case ext.data:
                    json.dump(files[f"{path}"], read(f"{path}", "w"), indent=4)
                case ext.image:
                    pygame.image.save(files[f"{path}"], f"{path}")
                case ext.text:
                    read(f"{path}", "w").write(files[f"{path}"])
                case _:
                    console.warn(f"Can't write, unknown extension '{"."+path.split(".")[-1]}'.")
            
        except KeyError:
            console.warn(f"Can't write {path}, not in memory.")


def ask(paths:list[str]) -> list[object]:
    read([path for path in paths if path not in files])
    return [files.get(path, None) for path in paths]


def directory(paths:list[str]) -> None:
    for path in paths:
        try:
            os.makedirs(f"{path}")
        except OSError:
            pass

def find(paths:list[str]) -> list[bool]:
    result = []
    for path in paths:
        result.append(os.path.exists(f"{path}"))
    return result