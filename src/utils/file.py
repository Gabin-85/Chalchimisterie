from args import ext
from utils.console import console
import json, pygame, os, copy

class file:

    files = {}
        
    @staticmethod
    def create(path:str, **kwargs) -> None|object:
        """
        Create a file

        Args:
            path (str): The path
            rebound (bool): The return option

        Returns:
            object (if rebound=True): The file
        """
        file.files[f"{path}"] = kwargs.get("data")
        if kwargs.get("rebound", False):
            return file.files[f"{path}"]

    @staticmethod
    def close(path:str) -> None:
        """
        Close a file

        Args:
            path (str): The path
            ext (str): The extension
        """
        try:
            del(file.files[f"{path}"])
        except KeyError:
            pass
        
    @staticmethod
    def copy(old_path:str, new_path:str, **kwargs) -> None|object:
        """
        Copy a file

        Args:
            old_path (str): The old path
            new_path (str): The new path
            rebound (bool): The return option

        Returns:
            object (if rebound=True): The file
        """
        if f"{old_path}" not in file.files:
            console.warn(f"Can't find the file '{old_path}' in memory.")
            return

        file.files[f"{new_path}"] = copy.deepcopy(file.files[f"{old_path}"])
        if kwargs.get("rebound", False):
            return file.files[f"{old_path}"]
    


    @staticmethod
    def open(path:str, **kwargs) -> None|object:
        """
        Open a file

        Args:
            path (str): The path
            rebound (bool): The return option

        Returns:
            object (if rebound=True): The file
        """
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

            if kwargs.get("rebound", False):
                return file.files[f"{path}"]
            
        except FileNotFoundError:
            console.warn(f"File {path} not found.")

    @staticmethod
    def delete(path:str) -> None:
        """
        Delete a file

        Args:
            path (str): the path
        """
        try:
            os.remove(f"{path}")
        except FileNotFoundError:
            pass

    @staticmethod
    def write(path:str, **kwargs) -> None|object:
        """
        Write a file

        Args:
            path (str): The path
            rebound (bool): The return option

        Returns:
            object (if rebound=True): The file
        """
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

            if kwargs.get("rebound", False):
                return file.files[f"{path}"]
            
        except KeyError:
            console.warn(f"Can't write {path}, not in memory.")



    @staticmethod
    def ask(path:str) -> object:
        """
        Ask a file

        Args:
            path (str): The 
            
        Return:
            object: The file
        """
        if path in file.files:
            return file.files[path]
        
        file.open(path)
        if path in file.files:
            return file.files[path]
        
        console.warn(f"File {path} not found.")


    @staticmethod
    def directory(path:str) -> None:
        """
        Create a folder

        Args:
            path (str): The path
        """
        try:
            os.makedirs(f"{path}")
        except OSError:
            pass
        
    @staticmethod
    def find(path:str) -> bool:
        """
        Check file existance in storage

        Args:
            path (str): The path

        Returns:
            bool: True if the file exists, False otherwise
        """
        return os.path.exists(f"{path}")