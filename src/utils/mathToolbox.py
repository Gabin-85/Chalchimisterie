###########
# VECTORS #
###########
    
class Vector2D:

    def __init__(self, x:float=0, y:float=0) -> None:
        self.x:float = x
        self.y:float = y

    def __repr__(self) -> str:
        """Get the string representation of the vector"""
        return "Vector2D(x='{}', y='{}')".format(self.x, self.y)

    def __copy__(self) -> 'Vector2D':
        """Get a copy of the vector"""
        return Vector2D(self.x, self.y)

    #############
    # Operators #
    #############
    def __add__(self, object:'Vector2D') -> 'Vector2D':
        """Add the vector"""
        return Vector2D(self.x + object.x, self.y + object.y)
    
    def __iadd__(self, object:'Vector2D') -> 'Vector2D':
        """Add the vector"""
        self.x += object.x
        self.y += object.y
        return self

    def __sub__(self, object:'Vector2D') -> 'Vector2D':
        """Subtract the vector"""
        return Vector2D(self.x - object.x, self.y - object.y)
    
    def __isub__(self, object:'Vector2D') -> 'Vector2D':
        """Subtract the vector"""
        self.x -= object.x
        self.y -= object.y
        return self
    
    def __mul__(self, object:'Vector2D') -> 'Vector2D':
        """Multiply the vector"""
        return Vector2D(self.x * object.x, self.y * object.y)
    
    def __imul__(self, object:'Vector2D') -> 'Vector2D':
        """Multiply the vector"""
        self.x *= object.x
        self.y *= object.y
        return self

    def __truediv__(self, object:'Vector2D') -> 'Vector2D':
        """Divide the vector"""
        return Vector2D(self.x / object.x, self.y / object.y)
    
    def __itruediv__(self, object:'Vector2D') -> 'Vector2D':
        """Divide the vector"""
        self.x /= object.x
        self.y /= object.y
        return self

    ###############
    # Equivalence #
    ###############
    def __eq__(self, object:'Vector2D') -> bool:
        """Get the equal vector"""
        return self.x == object.x and self.y == object.y
    
    def __ne__(self, object:'Vector2D') -> bool:
        """Get the not equal vector"""
        return self.x != object.x or self.y != object.y
    
    def __lt__(self, object:'Vector2D') -> bool:
        """Get the less than vector"""
        return self.x < object.x and self.y < object.y
    
    def __gt__(self, object:'Vector2D') -> bool:
        """Get the greater than vector"""
        return self.x > object.x and self.y > object.y
    
    def __le__(self, object:'Vector2D') -> bool:
        """Get the less or equal vector"""
        return self.x <= object.x and self.y <= object.y
    
    def __ge__(self, object:'Vector2D') -> bool:
        """Get the greater or equal vector"""
        return self.x >= object.x and self.y >= object.y
    
    ###########
    # Methods #
    ###########
    def length(self) -> float:
        """Get the length of the vector"""
        return (self.x**2 + self.y**2)**0.5
    
    def normalize(self) -> 'Vector2D':
        """Get a normalized vector"""
        length = self.length()
        if length != 0:
            return Vector2D(self.x / length, self.y / length)
        else:
            return Vector2D(0, 0)
    
    def inormalize(self) -> None:
        """Set an inormalized vector"""
        length = self.length()
        if length != 0:
            self.x /= length
            self.y /= length

    def scale(self, factor:float) -> 'Vector2D':
        """Get a scaled vector"""
        return Vector2D(self.x * factor, self.y * factor)
    
    def iscale(self, factor:float) -> None:
        """Set an iscaled vector"""
        self.x *= factor
        self.y *= factor

    def dot(self, object:'Vector2D') -> float:
        """Get the dot product of the vector"""
        return self.x * object.x + self.y * object.y
    
class Vector3D:

    def __init__(self, x:float=0, y:float=0, z:float=0) -> None:
        self.x:float = x
        self.y:float = y
        self.z:float = z

    def __repr__(self) -> str:
        """Get the string representation of the vector"""
        return "Vector3D(x='{}', y='{}', z='{}')".format(self.x, self.y, self.z)
    
    def __copy__(self) -> 'Vector3D':
        """Get a copy of the vector"""
        return Vector3D(self.x, self.y, self.z)
    
    #############
    # Operators #
    #############
    def __add__(self, object:'Vector3D') -> 'Vector3D':
        """Add the vector"""
        return Vector3D(self.x + object.x, self.y + object.y, self.z + object.z)
    
    def __iadd__(self, object:'Vector3D') -> 'Vector3D':
        """Add the vector"""
        self.x += object.x
        self.y += object.y
        self.z += object.z
        return self
    
    def __sub__(self, object:'Vector3D') -> 'Vector3D':
        """Subtract the vector"""
        return Vector3D(self.x - object.x, self.y - object.y, self.z - object.z)
    
    def __isub__(self, object:'Vector3D') -> 'Vector3D':
        """Subtract the vector"""
        self.x -= object.x
        self.y -= object.y
        self.z -= object.z
        return self
    
    def __mul__(self, object:'Vector3D') -> 'Vector3D':
        """Multiply the vector"""
        return Vector3D(self.x * object.x, self.y * object.y, self.z * object.z)
    
    def __imul__(self, object:'Vector3D') -> 'Vector3D':
        """Multiply the vector"""
        self.x *= object.x
        self.y *= object.y
        self.z *= object.z
        return self
    
    def __truediv__(self, object:'Vector3D') -> 'Vector3D':
        """Divide the vector"""
        return Vector3D(self.x / object.x, self.y / object.y, self.z / object.z)
    
    def __itruediv__(self, object:'Vector3D') -> 'Vector3D':
        """Divide the vector"""
        self.x /= object.x
        self.y /= object.y
        self.z /= object.z
        return self
    
    ###############
    # Equivalence #
    ###############
    def __eq__(self, object:'Vector3D') -> bool:
        """Get the equal vector"""
        return self.x == object.x and self.y == object.y and self.z == object.z
    
    def __ne__(self, object:'Vector3D') -> bool:
        """Get the not equal vector"""
        return self.x != object.x or self.y != object.y or self.z != object.z
    
    def __lt__(self, object:'Vector3D') -> bool:
        """Get the less than vector"""
        return self.x < object.x and self.y < object.y and self.z < object.z
    
    def __gt__(self, object:'Vector3D') -> bool:
        """Get the greater than vector"""
        return self.x > object.x and self.y > object.y and self.z > object.z
    
    def __le__(self, object:'Vector3D') -> bool:
        """Get the less or equal vector"""
        return self.x <= object.x and self.y <= object.y and self.z <= object.z
    
    def __ge__(self, object:'Vector3D') -> bool:
        """Get the greater or equal vector"""
        return self.x >= object.x and self.y >= object.y and self.z >= object.z
    
    ###########
    # Methods #
    ###########
    def length(self) -> float:
        """Get the length of the vector"""
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def normalize(self) -> 'Vector3D':
        """Get a normalized vector"""
        length = self.length()
        if length != 0:
            return Vector3D(self.x / length, self.y / length, self.z / length)
        else:
            return Vector3D(0, 0, 0)
    
    def inormalize(self) -> None:
        """Set an inormalized vector"""
        length = self.length()
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length

    def scale(self, factor:float) -> 'Vector3D':
        """Get a scaled vector"""
        return Vector3D(self.x * factor, self.y * factor, self.z * factor)
    
    def iscale(self, factor:float) -> None:
        """Set an iscaled vector"""
        self.x *= factor
        self.y *= factor
        self.z *= factor

    def dot(self, object) -> float:
        """Get the dot product of the vector"""
        return self.x * object.x + self.y * object.y + self.z * object.z
    
#########
# RECTS #
#########

class Rect2D:

    def __init__(self, x:float=0, y:float=0, width:float=0, height:float=0) -> None:
        self.x:float = x
        self.y:float = y
        self.width:float = width
        self.height:float = height

    def __repr__(self) -> str:
        return "Rect2D(x='{}', y='{}', width='{}', height='{}')".format(self.x, self.y, self.width, self.height)
    
    def __copy__(self) -> 'Rect2D':
        return Rect2D(self.x, self.y, self.width, self.height)
    
    #############
    # Operators #
    #############
    def __add__(self, object:Vector2D) -> 'Rect2D':
        """Move a 2d vector"""
        return Rect2D(self.x + object.x, self.y + object.y, self.width, self.height)
    
    def __iadd__(self, object:Vector2D) -> 'Rect2D':
        """Move a 2d vector"""
        self.x += object.x
        self.y += object.y
        return self
    
    def __sub__(self, object:Vector2D) -> 'Rect2D':
        """Move a 2d vector"""
        return Rect2D(self.x - object.x, self.y - object.y, self.width, self.height)
    
    def __isub__(self, object:Vector2D) -> 'Rect2D':
        """Move a 2d vector"""
        self.x -= object.x
        self.y -= object.y
        return self
    
    def __mul__(self, object:Vector2D) -> 'Rect2D':
        """Scale a 2d vector"""
        return Rect2D(self.x, self.y, object.x, object.y)
    
    def __imul__(self, object:Vector2D) -> 'Rect2D':
        """Scale a 2d vector"""
        self.width = object.x
        self.height = object.y
        return self
    
    def __truediv__(self, object:Vector2D) -> 'Rect2D':
        """Scale a 2d vector"""
        return Rect2D(self.x, self.y, -object.x, -object.y)
    
    def __itruediv__(self, object:Vector2D) -> 'Rect2D':
        """Scale a 2d vector"""
        self.width = -object.x
        self.height = -object.y
        return self

    ###########
    # Methods #
    ###########

    def get_center(self) -> Vector2D:
        """Get the center of the rect"""
        return Vector2D(self.x + self.width / 2, self.y + self.height / 2)
    
    def set_center(self, center:Vector2D) -> None:
        """Set the center of the rect"""
        self.x = center.x - self.width / 2
        self.y = center.y - self.height / 2
    
    def collide_point(self, point:Vector2D) -> bool:
        """Check if the point is in the rect"""
        return self.x <= point.x and self.y <= point.y and self.x + self.width >= point.x and self.y + self.height >= point.y
    
    def collide_rect(self, rect) -> bool:
        """Check if the rect is in the rect"""
        return (self.x + self.width >= rect.x) and (self.x <= rect.x + rect.width) and (self.y + self.height >= rect.y) and (self.y <= rect.y + rect.height)
    
class Rect3D():

    def __init__(self, x:float=0, y:float=0, z:float=0, width:float=0, height:float=0, depth:float=0) -> None:
        self.x:float = x
        self.y:float = y
        self.z:float = z
        self.width:float = width
        self.height:float = height
        self.depth:float = depth

    def __repr__(self) -> str:
        return "Rect3D(x='{}', y='{}', z='{}', width='{}', height='{}', depth='{}')".format(self.x, self.y, self.z, self.width, self.height, self.depth)
    
    def __copy__(self) -> 'Rect3D':
        return Rect3D(self.x, self.y, self.z, self.width, self.height, self.depth)
    
    #############
    # Operators #
    #############

    def __add__(self, object:Vector3D) -> 'Rect3D':
        """Move a 3d vector"""
        return Rect3D(self.x + object.x, self.y + object.y, self.z + object.z, self.width, self.height, self.depth)
    
    def __iadd__(self, object:Vector3D) -> 'Rect3D':
        """Move a 3d vector"""
        self.x += object.x
        self.y += object.y
        self.z += object.z
        return self
    
    def __sub__(self, object:Vector3D) -> 'Rect3D':
        """Move a 3d vector"""
        return Rect3D(self.x - object.x, self.y - object.y, self.z - object.z, self.width, self.height, self.depth)
    
    def __isub__(self, object:Vector3D) -> 'Rect3D':
        """Move a 3d vector"""
        self.x -= object.x
        self.y -= object.y
        self.z -= object.z
        return self
    
    def __mul__(self, object:Vector3D) -> 'Rect3D':
        """Scale a 3d vector"""
        return Rect3D(self.x, self.y, self.z, object.x, object.y, object.z)
    
    def __imul__(self, object:Vector3D) -> 'Rect3D':
        """Scale a 3d vector"""
        self.width = object.x
        self.height = object.y
        self.depth = object.z
        return self

    def __truediv__(self, object:Vector3D) -> 'Rect3D':
        """Scale a 3d vector"""
        return Rect3D(self.x, self.y, self.z, -object.x, -object.y, -object.z)
    
    def __itruediv__(self, object:Vector3D) -> 'Rect3D':
        """Scale a 3d vector"""
        self.width = -object.x
        self.height = -object.y
        self.depth = -object.z
        return self
    
    ###########
    # Methods #
    ###########

    def get_center(self) -> Vector3D:
        """Get the center of the rect"""
        return Vector3D(self.x + self.width / 2, self.y + self.height / 2, self.z + self.depth / 2)
    
    def set_center(self, center:Vector3D) -> None:
        """Set the center of the rect"""
        self.x = center.x - self.width / 2
        self.y = center.y - self.height / 2
        self.z = center.z - self.depth / 2

    def collide_point(self, point:Vector3D) -> bool:
        """Check if the point is in the rect"""
        return self.x <= point.x and self.y <= point.y and self.z <= point.z and self.x + self.width >= point.x and self.y + self.height >= point.y and self.z + self.depth >= point.z
    
    def collide_rect(self, rect:'Rect3D') -> bool:
        """Check if the rect is in the rect"""
        return (self.x + self.width >= rect.x) and (self.x <= rect.x + rect.width) and (self.y + self.height >= rect.y) and (self.y <= rect.y + rect.height) and (self.z + self.depth >= rect.z) and (self.z <= rect.z + rect.depth)