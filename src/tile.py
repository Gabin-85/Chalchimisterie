import pygame

def tile_map_draw(dict:dict, name:list, x:list, y:list):
    """
    Draw all tiles in a dictionary

    Args:
        dict (dict): dictionary of tiles
        name (list): name of the tiles
        x (list): x position of the tiles
        y (list): y position of the tiles

    Returns:
        (list) : image (the tile and parameter of the tile)
    """
    image = [[],[],[]]
    for tile in range(len(name)):
        # Get the tile from the image
        image_object = pygame.image.load(dict["texture"])
        image_size = image_object.get_size()
        surface = pygame.Surface(image_size)
        clip = pygame.Rect(dict[name[tile]][0]*dict["size"], dict[name[tile]][1]*dict["size"], dict["size"], dict["size"])
        surface.set_clip(clip)
        image_object = image_object.subsurface(surface.get_clip())
        # Set the image and the position of the tile
        image[0].append(image_object.copy())
        image[1].append(x[tile]*dict["size"])
        image[2].append(y[tile]*dict["size"])
    return image
        

    