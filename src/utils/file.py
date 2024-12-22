from args import ext
from utils.console import console
import json, pygame, os, copy

class file:

    files = {}
        
    @staticmethod
    def create(*paths:str, data=None) -> None:
        """
        Create files

        Args:
            paths (str): The paths
            data (any): The data
            
        """
        for path in paths:
            file.files[f"{path}"] = data

    @staticmethod
    def close(*paths:str) -> None:
        """
        Close files

        Args:
            paths (str): The paths
        """
        for path in paths:
            try:
                file.files[f"{path}"]
            except KeyError:
                pass
        
    @staticmethod
    def copy(old_path:str, *new_paths:str) -> None:
        """
        Copy files

        Args:
            old_path (str): The old path
            new_paths (str): The new paths
        """
        if f"{old_path}" not in file.files:
                console.warn(f"Can't find the file '{old_path}' in memory.")
                return
        
        for new_path in new_paths:
            file.files[f"{new_path}"] = copy.deepcopy(file.files[f"{old_path}"])
    
    @staticmethod
    def open(*paths:str) -> None:
        """
        Open files

        Args:
            paths (str): The paths
        """
        for path in paths:
            try:
                match "."+path.split(".")[-1]:
                    case ext.data:
                        file.files[f"{path}"] = json.load(open(f"{path}", "r"))
                    case ext.image:
                        file.files[f"{path}"] = pygame.image.load(f"{path}")
                    case ext.text:
                        file.files[f"{path}"] = open(f"{path}", "r").read()
                    case _:
                        file.files[f"{path}"] = None
                        console.warn(f"Can't open, unknown extension '{"."+path.split(".")[-1]}'.")
                
            except FileNotFoundError:
                console.warn(f"File {path} not found.")

    @staticmethod
    def delete(*paths:str) -> None:
        """
        Delete files

        Args:
            paths (str): The paths
        """
        for path in paths:
            try:
                os.remove(f"{path}")
            except FileNotFoundError:
                pass

    @staticmethod
    def write(*paths:str) -> None:
        """
        Write files

        Args:
            paths (str): The paths
        """
        for path in paths:
            try:
                match "."+path.split(".")[-1]:
                    case ext.data:
                        json.dump(file.files[f"{path}"], open(f"{path}", "w"), indent=4)
                    case ext.image:
                        pygame.image.save(file.files[f"{path}"], f"{path}")
                    case ext.text:
                        open(f"{path}", "w").write(file.files[f"{path}"])
                    case _:
                        console.warn(f"Can't write, unknown extension '{"."+path.split(".")[-1]}'.")
                
            except KeyError:
                console.warn(f"Can't write {path}, not in memory.")

    @staticmethod
    def ask(*paths:str) -> list[object]:
        """
        Ask files

        Args:
            paths (str): The paths
            
        Return:
            list[object]: The files
        """
        result = []
        for path in paths:
            if path not in file.files:
                file.open(path)

            try:
                result.append(file.files[path])
            except KeyError:
                console.warn(f"File {path} not found.")
                result.append(None)

        return result


    @staticmethod
    def directory(*paths:str) -> None:
        """
        Create folders

        Args:
            path (str): The path
        """
        for path in paths:
            try:
                os.makedirs(f"{path}")
            except OSError:
                pass
        
    @staticmethod
    def find(*paths:str) -> list[bool]:
        """
        Check if files exists

        Args:
            path (str): The path

        Return:
            list[bool]: True if the files exists, false otherwise
        """
        result = []
        for path in paths:
            result.append(os.path.exists(f"{path}"))

        return result