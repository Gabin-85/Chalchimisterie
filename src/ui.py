import pyglet

class SpriteRect:

    def __init__(self) -> None:
        """
        Create a drawing rect
        """
        self.batch:pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.sprites:list[pyglet.sprite.Sprite] = []

    def add_sprite(self, sprites:list[pyglet.sprite.Sprite]) -> None:
        """
        Add sprites to the group

        Args:
            sprites (pyglet.sprite.Sprite): Sprites to add
        """
        for sprite in sprites:
            sprite.batch = self.batch
            self.sprites.append(sprite)

    def set_size(self, width:int, height:int) -> None:
        """
        Change the size of the rect

        Args:
            width (int): The new width
            height (int): The new height
        """
        for sprite in self.sprites:
            sprite.x = sprite.x * width/sprite.width
            sprite.y = sprite.y * height/sprite.height
            sprite.width = width
            sprite.height = height
            

    def add_offset(self, x:int, y:int) -> None:
        """
        Change the coordinates of the rect

        Args:
            x (int): The new x coordinate
            y (int): The new y coordinate
        """
        for sprite in self.sprites:
            sprite.x += x
            sprite.y += y

    def draw(self) -> None:
        """
        Draw the objects in the batch
        """
        self.batch.draw()


class ui:
    
    pages:dict = {}

    @staticmethod
    def create(page_name:str, page_type:str, parent = None) -> None:
        """
        Create a new page

        Args:
            page_name (str): The name of the page
            page_type (str): The type of the page
            parent (str, optional): The parent of the page. Defaults to None.
        """
        pass