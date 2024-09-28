from args import pathLocation, fileExtension
from utils.console import console
import json, pyglet, os, copy

class file:

    files = {}

    @staticmethod
    def open(directory:pathLocation|str, filename:str, extension:fileExtension) -> object|None:
        """
        Open a file from disc to the cache

        Args:
            directory (str): The directory of the file
            filename (str): The name of the file
            extension (str): The extension of the file

        Returns:
            An address of the cached file

        Raises:
            FileNotFoundError: If the file doesn't exist
            KeyError: If the file extension is invalid
        """
        if f"{directory}{filename}{extension}" in file.files:
            return file.files[f"{directory}{filename}{extension}"]
        
        try:
            match extension:
                case fileExtension.data:
                    file.files[f"{directory}{filename}{extension}"] = json.load(open(f"{directory}{filename}{extension}", "r"))
                case fileExtension.image:
                    file.files[f"{directory}{filename}{extension}"] = pyglet.image.load(f"{directory}{filename}{extension}")
                case fileExtension.text:
                    file.files[f"{directory}{filename}{extension}"] = open(f"{directory}{filename}{extension}", "r").read()
            return file.files[f"{directory}{filename}{extension}"]
        except FileNotFoundError:
            console.warn(f"File {directory}{filename}{extension} not found")
        except KeyError:
            console.warn(f"Can't load {directory}{filename}{extension}. Invalid extension")

    @staticmethod
    def add(directory:pathLocation|str, filename:str, extension:fileExtension, data = None) -> object:
        """
        Create a file from a variable to the cache

        Args:
            directory (str): The directory of the file
            filename (str): The name of the file
            extension (str): The extension of the file
            data (any): The data to save

        Returns:
            An address of the cached file
        """
        file.files[f"{directory}{filename}{extension}"] = data
        return file.files[f"{directory}{filename}{extension}"]
    
    @staticmethod
    def write(directory:pathLocation|str, filename:str, extension:fileExtension) -> object|None:
        """
        Write a file from the cache to the disc

        Args:
            directory (str): The directory of the file
            filename (str): The name of the file
            extension (str): The extension of the file

        Returns:
            An address of the cached file
            
        Raises:
            KeyError: If the file isn't in the cache
        """
        try:
            match extension:
                case fileExtension.data:
                    json.dump(file.files[f"{directory}{filename}{extension}"], open(f"{directory}{filename}{extension}", "w"), indent=4)
                case fileExtension.image:
                    file.files[f"{directory}{filename}{extension}"].save(f"{directory}{filename}{extension}")
                case fileExtension.text:
                    open(f"{directory}{filename}{extension}", "w").write(file.files[f"{directory}{filename}{extension}"])
            return file.files[f"{directory}{filename}{extension}"]
        except KeyError:
            console.warn(f"Can't write {directory}{filename}{extension}. It's not in the cache")
        
    @staticmethod
    def copy(original_directory:pathLocation|str, original_filename:str, copied_directory:pathLocation|str, copied_filename:str, extension:fileExtension) -> object|None:
        """
        Copy a file from the disc or the cache to the cache

        Args:
            original_directory (str): The directory of the original file
            original_filename (str): The name of the original file
            copied_directory (str): The directory of the copied file
            copied_filename (str): The name of the new copied file
            extension (str): The extension of the file

        Returns:
            An address of the cached file
            
        Raises:
            KeyError: If the file isn't in the cache
        """
        if original_filename == copied_filename and original_directory == copied_directory:
            console.warn(f"Can't copy {original_filename} to itself")
            return

        if f"{original_directory}{original_filename}{extension}" in file.files:
            file.files[f"{copied_directory}{copied_filename}{extension}"] = copy.deepcopy(file.files[f"{original_directory}{original_filename}{extension}"])
            return file.files[f"{copied_directory}{copied_filename}{extension}"]
        
        try:
            match extension:
                case fileExtension.data:
                    file.files[f"{copied_directory}{copied_filename}{extension}"] = json.load(open(f"{original_directory}{original_filename}{extension}", "r"))
                case fileExtension.image:
                    file.files[f"{copied_directory}{copied_filename}{extension}"] = pyglet.image.load(f"{original_directory}{original_filename}{extension}")
                case fileExtension.text:
                    file.files[f"{copied_directory}{copied_filename}{extension}"] = open(f"{original_directory}{original_filename}{extension}", "r").read()
            return file.files[f"{copied_directory}{copied_filename}{extension}"]
        except FileNotFoundError:
            console.warn(f"File {original_directory}{original_filename}{extension} not found")
        except KeyError:
            console.warn(f"Can't load {original_directory}{original_filename}{extension}. Invalid extension")

    @staticmethod
    def close(directory:pathLocation|str, filename:str, extension:fileExtension) -> bool:
        """
        Delete a file in the cache

        Args:
            directory (str): The directory of the file
            filename (str): The name of the file
            extension (str): The extension of the file

        Returns:
            bool: True if the file was deleted, False otherwise
        """
        try:
            del(file.files[f"{directory}{filename}{extension}"])
            return True
        except KeyError:
            return False

    @staticmethod
    def sup(directory:pathLocation|str, filename:str, extension:fileExtension) -> bool:
        """
        Delete a file in the disc

        Args:
            directory (str): The directory of the file
            filename (str): The name of the file
            extension (str): The extension of the file

        Returns:
            bool: True if the file was deleted, False otherwise
        """
        try:
            os.remove(f"{directory}{filename}{extension}")
            return True
        except FileNotFoundError:
            return False
        
    @staticmethod
    def mkdir(folderpath:pathLocation|str, foldername:str) -> bool:
        """
        Create a directory in the disc

        Args:
            folderpath (str): The directory of the folder
            foldername (str): The name of the folder

        Returns:
            bool: True if the directory was created, False otherwise
        """
        try:
            if os.path.exists(f"{folderpath}") == False or os.path.exists(f"{folderpath}{foldername}") == True:
                return False
            os.mkdir(f"{folderpath}{foldername}")
            return True
        except FileExistsError:
            return False
        
    @staticmethod
    def find(directory:pathLocation|str, filename:str, extension:fileExtension) -> bool:
        """
        Check if a file exists in the cache

        Args:
            directory (str): The directory of the file
            filename (str): The name of the file
            extension (str): The extension of the file

        Returns:
            bool: True if the file exists, False otherwise
        """
        return os.path.exists(f"{directory}{filename}{extension}")