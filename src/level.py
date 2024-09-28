from utils.console import console
from args import pathLocation, fileExtension
from utils.file import file
import pyglet

def get_tileset(tilemaps_index:list[str]) -> list:
    """
    Give a tileset from a list of tilemaps

    Args:
        tilemaps_index (list[str]): The list of tilemaps names

    Returns:
        list: The tileset
    """
    tileset:list = []

    for tilemap in tilemaps_index:

        console.trace(f"Loading tilemap '{tilemap}'")
        tilemap_config:dict = file.open(pathLocation.tilemap, tilemap, fileExtension.data)
        tilemap_image:pyglet.image.ImageData = file.open(pathLocation.tilemap, tilemap, fileExtension.image)

        if tilemap_config is None or tilemap_image is None:
            console.warn(f"tilemap_config or tilemap_image of {tilemap} not found")
            return
        
        for tile in tilemaps_index[tilemap]:
            x, y = tilemap_config["tiles"][tile]
            tileset.append(tilemap_image.get_region(x*tilemap_config["tilesize"], tilemap_image.height-(y+1)*tilemap_config["tilesize"], tilemap_config["tilesize"], tilemap_config["tilesize"]))

    return tileset

def get_level(level_name:str, batch:pyglet.graphics.Batch) -> list[pyglet.sprite.Sprite]:
    """
    Generates a list of images for a level

    Args:
        level_name (str): The name of the level

    Returns:
        images (list[pyglet.sprite.Sprite]): The list of images of the level
    """
    console.trace(f"Creating level '{level_name}'")
    level_config = file.open(pathLocation.level, level_name, fileExtension.data)
    level_sprites:list[pyglet.sprite.Sprite] = []
    tileset:list = None

    file.mkdir(pathLocation.layer, level_name)

    for layer_config in level_config["layers"]:

        if file.find(f"{pathLocation.layer}{level_name}/", layer_config["name"], fileExtension.image):
            console.trace(f"Loading layer '{layer_config["name"]}'")
            layer_image:pyglet.image.ImageData = file.open(f"{pathLocation.layer}{level_name}/", layer_config["name"], fileExtension.image)
            
        else:
            console.trace(f"Creating layer '{layer_config["name"]}'")
            if tileset is None:
                tileset = get_tileset(level_config["tilemap_index"])

            layer_args:list = []
            for y in range(len(layer_config["layermap"])):
                for x in range(len(layer_config["layermap"][y])):
                    layer_args.append([layer_config["layermap"][y][x], x*level_config["tilesize"], (len(layer_config["layermap"])-y-1)*level_config["tilesize"]])

            layer_image:pyglet.image.Texture = file.add(f"{pathLocation.layer}{level_name}/", layer_config["name"], fileExtension.image, pyglet.image.Texture.create(len(layer_config["layermap"][0])*level_config["tilesize"], len(layer_config["layermap"])*level_config["tilesize"]))
            for tile in range(len(layer_args)):
                layer_image.blit_into(tileset[layer_args[tile][0]], layer_args[tile][1], layer_args[tile][2], 0)

            file.write(f"{pathLocation.layer}{level_name}/", layer_config["name"], fileExtension.image)

        level_sprites.append(pyglet.sprite.Sprite(layer_image, x=layer_config["coord"][0]*level_config["tilesize"], y=-layer_config["coord"][1]*level_config["tilesize"], batch=batch))

    return level_sprites, batch