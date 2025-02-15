import pygame
from typing import Union

class Vector2(pygame.Vector2):
    
    def __lt__(self, vector:'Vector2') -> bool:
        return self.x < vector.x and self.y < vector.y
    
    def __le__(self, vector:'Vector2') -> bool:
        return self.x <= vector.x and self.y <= vector.y
    
    def __gt__(self, vector:'Vector2') -> bool:
        return self.x > vector.x and self.y > vector.y
    
    def __ge__(self, vector:'Vector2') -> bool:
        return self.x >= vector.x and self.y >= vector.y

class Vector3(pygame.Vector3):
    
    def __lt__(self, vector:'Vector3') -> bool:
        return self.x < vector.x and self.y < vector.y and self.z < vector.z
    
    def __le__(self, vector:'Vector3') -> bool:
        return self.x <= vector.x and self.y <= vector.y and self.z <= vector.z
    
    def __gt__(self, vector:'Vector3') -> bool:
        return self.x > vector.x and self.y > vector.y and self.z > vector.z
    
    def __ge__(self, vector:'Vector3') -> bool:
        return self.x >= vector.x and self.y >= vector.y and self.z >= vector.z

class Boxe2:

    def __init__(self, position:Vector2, size:Vector2) -> None:
        self.position = position
        self.size = size

    def __repr__(self):
        return str(f"[{self.position}, {self.size}]")

    def copy(self):
        return Boxe2(self.position, self.size)

    def move(self, move:Vector2) -> None:
        self.position += move

    def move_to(self, position:Vector2) -> None:
        self.position = position

    def scale(self, scale:float) -> None:
        self.size *= scale

    def scale_to(self, size:Vector2) -> None:
        self.size = size

    def set_center(self, position:Vector2) -> None:
        self.position = position-self.size*0.5

    def get_center(self) -> Vector2:
        return self.position+self.size*0.5

    def collide_point(self, point:Vector2) -> bool:
        return self.position < point and point < self.position+self.size
    
    def collide_boxe(self, boxe:'Boxe2') -> bool:
        return boxe.position < self.position+self.size and self.position < boxe.position+boxe.size

class Boxe3:

    def __init__(self, position:Vector3, size:Vector3) -> None:
        self.position = position
        self.size = size

    def __repr__(self):
        return str(f"[{self.position}, {self.size}]")

    def copy(self):
        return Boxe3(self.position, self.size)

    def move(self, move:Vector3) -> None:
        self.position += move

    def move_to(self, position:Vector3) -> None:
        self.position = position

    def scale(self, scale:float) -> None:
        self.size *= scale

    def scale_to(self, size:Vector3) -> None:
        self.size = size

    def set_center(self, position:Vector3) -> None:
        self.position = position-self.size*0.5

    def get_center(self) -> Vector3:
        return self.position+self.size*0.5

    def collide_point(self, point:Vector3) -> bool:
        return self.position < point and point < self.position+self.size
    
    def collide_boxe(self, boxe:'Boxe3') -> bool:
        return boxe.position < self.position+self.size and self.position < boxe.position+boxe.size

vector2:list[Vector2] = []
vector3:list[Vector3] = []
boxe2:list[Boxe2] = []
boxe3:list[Boxe3] = []

def new_vector2(x:float, y:float) -> int:
    vector2.append(Vector2(x, y))
    return len(vector2)-1

def new_vector3(x:float, y:float, z:float) -> int:
    vector3.append(Vector3(x, y, z))
    return len(vector3)-1

def new_boxe2(position:Union[float, Vector2], size:Union[float, Vector2]) -> int:
    if isinstance(position, tuple) and isinstance(size, tuple):
        boxe2.append(Boxe2(Vector2(*position), Vector2(*size)))
    else:
        boxe2.append(Boxe2(position, size))
    return len(boxe2)-1

def new_boxe3(position:Union[float, Vector2], size:Union[float, Vector2]) -> int:
    if isinstance(position, tuple) and isinstance(size, tuple):
        boxe3.append(Boxe3(Vector3(*position), Vector3(*size)))
    else:
        boxe3.append(Boxe3(position, size))
    return len(boxe3)-1

def get_vector2_by_name(name:str) -> list[int]:
    return [vector2.index(vector) for vector in vector2 if vector["name"] == name]

def get_vector3_by_name(name:str) -> list[int]:
    return [vector3.index(vector) for vector in vector3 if vector["name"] == name]

def get_boxe2_by_name(name:str) -> list[int]:
    return [boxe2.index(boxe) for boxe in boxe2 if boxe["name"] == name]

def get_boxe3_by_name(name:str) -> list[int]:
    return [boxe3.index(boxe) for boxe in boxe3 if boxe["name"] == name]