from utils.console import console
from args import pathLocation, fileExtension
from file import file
import pyglet, cProfile

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
        tilemap_config:dict = file.open(pathLocation.tilemap_config, tilemap, fileExtension.data)
        tilemap_image:pyglet.image.ImageData = file.open(pathLocation.tilemap_image, tilemap, fileExtension.image)

        if tilemap_config is None or tilemap_image is None:
            console.warn(f"tilemap_config or tilemap_image of {tilemap} not found")
            return
        
        for tile in tilemaps_index[tilemap]:
            x, y = tilemap_config["tiles"][tile]
            tileset.append(tilemap_image.get_region(x*tilemap_config["tilesize"], tilemap_image.height-(y+1)*tilemap_config["tilesize"], tilemap_config["tilesize"], tilemap_config["tilesize"]))

    return tileset

def get_layer(layer_name:str) -> list[pyglet.image.Texture]:
    """
    Give a layer from the layer name

    Args:
        layer_name (str): The name of the layer

    Returns:
        list: The layer image
    """

    if file.find(pathLocation.layer_image, layer_name, fileExtension.image):
        console.trace(f"Loading layer image '{layer_name}'")
        return file.open(pathLocation.layer_image, layer_name, fileExtension.image).get_texture()

    console.trace(f"Creating layer image '{layer_name}'")
    layer_config = file.open(pathLocation.layer_config, layer_name, fileExtension.data)

    tileset = get_tileset(layer_config["tilemap_index"])
    if tileset is None:
        return

    layer_arguments = []
    for y in range(len(layer_config["layermap"])):
        for x in range(len(layer_config["layermap"][y])):
            layer_arguments.append([layer_config["layermap"][y][x], x*layer_config["tilesize"], (len(layer_config["layermap"])-y-1)*layer_config["tilesize"]])

    layer_image:pyglet.image.Texture = file.add(pathLocation.layer_image, layer_config["name"], fileExtension.image, pyglet.image.Texture.create(len(layer_config["layermap"][0])*layer_config["tilesize"], len(layer_config["layermap"])*layer_config["tilesize"]))
    for tile in range(len(layer_arguments)):
        layer_image.blit_into(tileset[layer_arguments[tile][0]], layer_arguments[tile][1], layer_arguments[tile][2], 0)

    file.add(pathLocation.layer_config, layer_config["name"], fileExtension.data, layer_config)
    return file.write(pathLocation.layer_image, layer_config["name"], fileExtension.image)

def get_level(level_name:str) -> list[list[pyglet.sprite.Sprite], pyglet.graphics.Batch]:
    """
    Generates a batch and a list of images for a level

    Args:
        level_name (str): The name of the level

    Returns:
        images (list[pyglet.sprite.Sprite]): The list of images of the level
        batch (pyglet.sprite.Batch): The batch of the level
    """
    console.trace(f"Creating level '{level_name}'")
    level_config = file.open(pathLocation.level_config, level_name, fileExtension.data)
    images:list[pyglet.sprite.Sprite] = []
    batch = pyglet.graphics.Batch()

    for layer in level_config["layer"]:
        layer_image:pyglet.image.ImageData = get_layer(layer[0]).get_image_data()
        images.append(pyglet.sprite.Sprite(layer_image, x=layer[1], y=layer[2], batch=batch))

    return images, batch