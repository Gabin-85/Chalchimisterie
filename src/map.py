from dataclasses import dataclass
import pygame, pytmx, pyscroll

# Creation of the datclass Map.
# A data class is a class where you won't find any methods but data declaration.
# The @dataclass decorator is used to create the dataclass (the __init__ section here).
@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]        # Little secrete of what's coming next.
    group: pyscroll.PyscrollGroup

class MapManager:

    def __init__(self, screen):
        # Here we create the map manager.
        # "object" -> Map("object", walls, group)
        self.folder_path = "assets/maps/"
        self.current_map = "test"
        self.maps = dict()
        self.screen = screen

        self.register_map("test")

    def register_map(self, name):
        """
        Register a map: load the map and create the group.

        Args:
            name (str): name of the map.
        """

        # Load map (tmx file)
        tmx_data = pytmx.util_pygame.load_pygame(self.folder_path+f"{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # Create the group (assembling layers)
        group = pyscroll.PyscrollGroup(map_layer, default_layer=1)

        # Create the map
        self.maps[name] = Map(name, [], group)

    def get_map(self): 
        return self.maps[self.current_map]
    
    def get_group(self):
        return self.get_map().group
    
    def get_walls(self):
        return self.get_map().walls

    def update(self):
        self.get_group().update()