from utils.resourcesHandler import storage, save
from utils.mathToolbox import Vector2D, Rect2D
from utils.entityHandler import entity_handler
from utils.timeToolbox import Timer
from utils.consoleSystem import warn
import pygame

class Entity(pygame.sprite.Sprite):

    def __init__ (self) -> None:
        super().__init__()
        self.name = None
        self.id = None
        self.save = None

    def create(self, name, pattern:str, position:Vector2D, scene_name, map_name):
        template = storage.get(pattern, "entities")

        # General
        self.id = len(entity_handler.entities)-1
        self.name = name
        self.pattern = pattern
        self.rect = pygame.Rect(0, 0, 0, 0)

        # Position
        self.scene_name:str = scene_name
        self.map_name:str = map_name
        self.position:Vector2D = position

        # Boxes
        self.hitbox:Rect2D = Rect2D(*template["hitbox"])
        self.hurtbox:Rect2D = Rect2D(*template["hurtbox"])

        # Physics
        self.velocity:Vector2D = Vector2D(*template["velocity"])
        self.acceleration:Vector2D = Vector2D(0, 0)
        self.mass:float = template["mass"]
        self.force:float = template["force"]
        self.friction:float = template["friction"]

        # Textures and animation
        self.texture:dict = storage.get(self.pattern, "animations")
        self.texture_image:pygame.image = pygame.image.load("assets/sprites/" + self.texture["file"])
        self.texture_size:list = self.texture["size"]
        self.texture_images:dict = {}

        self.animation:str = template["animation"]
        self.animation_frame:int = template["animation_frame"]
        self.animation_time:int = self.texture["time"]
        self.animation_timer:Timer = Timer(template["animation_timer"])

        for animation in self.texture["animations"].keys():
            self.texture_images[animation] = [None]*self.texture["animations"][animation]
            for frame in range(len(self.texture_images[animation])):
                self.texture_images[animation][frame] = [frame * self.texture_size[0], list(self.texture["animations"].keys()).index(animation) * self.texture_size[1], self.texture_size[0], self.texture_size[1]]

    def load(self, id:int):
        self.save = saveEntity(id)
        self.save.load(id)

        # General
        self.id = id
        self.name = self.save.get("name")
        self.pattern = self.save.get("pattern")
        self.rect = pygame.Rect(0, 0, 0, 0)

        # Position
        self.scene_name:str = self.save.get("scene_name")
        self.map_name:str = self.save.get("map_name")
        self.position:Vector2D = Vector2D(*self.save.get("position"))

        # Boxes
        self.hitbox:Rect2D = Rect2D(*self.save.get("hitbox"))
        self.hurtbox:Rect2D = Rect2D(*self.save.get("hurtbox"))

        # Physics
        self.velocity:Vector2D = Vector2D(*self.save.get("velocity"))
        self.acceleration:Vector2D = Vector2D(0, 0)
        self.mass:float = self.save.get("mass")
        self.force:float = self.save.get("force")
        self.friction:float = self.save.get("friction")

        # Textures and animation
        self.texture:dict = storage.get(self.pattern, "animations")
        self.texture_image:pygame.image = pygame.image.load("assets/sprites/" + self.texture["file"])
        self.texture_size:list = self.texture["size"]
        self.texture_images:dict = {}

        self.animation:str = self.save.get("animation")
        self.animation_frame:int = self.save.get("animation_frame")
        self.animation_time:int = self.texture["time"]
        self.animation_timer:Timer = Timer(self.save.get("animation_timer"))

        for animation in self.texture["animations"].keys():
            self.texture_images[animation] = [None]*self.texture["animations"][animation]
            for frame in range(len(self.texture_images[animation])):
                self.texture_images[animation][frame] = [frame * self.texture_size[0], list(self.texture["animations"].keys()).index(animation) * self.texture_size[1], self.texture_size[0], self.texture_size[1]]

    def unload(self):
        self.save = saveEntity(self.id)

        # General
        self.save.set("id", self.id)
        self.save.set("name", self.name)
        self.save.set("pattern", self.pattern)

        # Position
        self.save.set("scene_name", self.scene_name)
        self.save.set("map_name", self.map_name)
        self.save.set("position", [self.position.x, self.position.y])

        # Boxes
        self.save.set("hitbox", [self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height])
        self.save.set("hurtbox", [self.hurtbox.x, self.hurtbox.y, self.hurtbox.width, self.hurtbox.height])

        # Physics
        self.save.set("velocity", [self.velocity.x, self.velocity.y])
        self.save.set("mass", self.mass)
        self.save.set("force", self.force)
        self.save.set("friction", self.friction)

        # Animation
        self.save.set("animation", self.animation)
        self.save.set("animation_frame", self.animation_frame)
        self.save.set("animation_timer", self.animation_timer.remaining_time())

        self.save.unload()

    def start_animation(self):
        self.animation_timer.start()

    def stop_animation(self):
        self.animation_timer.stop()

    def change_animation(self, animation:str):
        if self.animation != animation:
            self.animation = animation
            self.animation_frame = -1
            self.animation_timer.reset(self.animation_time)

    def change_frame(self, frame:int=None) -> pygame.Rect:
        if self.animation_timer.check() or self.animation_frame == -1:
            if frame is None:
                frame = (self.animation_frame + 1) % len(self.texture_images[self.animation])
            if self.animation_frame != frame:
                self.image = pygame.Surface(self.texture_size)
                self.image.blit(self.texture_image, (0, 0), self.texture_images[self.animation][frame])
                self.image.set_colorkey((0, 0, 0))
                self.rect = self.image.get_rect()

    def update(self, dt:float):
        try:
            self.acceleration.scale(self.force/self.mass)
        except ValueError:
            self.acceleration = Vector2D(0, 0)
        self.velocity -= (self.velocity.scale(self.friction / self.mass) - self.acceleration).scale(dt)
        feetx = Rect2D(self.hitbox.x + self.velocity.x, self.hitbox.y, self.hitbox.width, self.hitbox.height)
        feety = Rect2D(self.hitbox.x, self.hitbox.y + self.velocity.y, self.hitbox.width, self.hitbox.height)

        from utils.loadHandler import load
        for wall in load.get_walls():
            if feetx.collide_rect(wall["rect"]) == True:
                match wall["collision_type"]:
                    case "bouncy":
                        self.velocity.x *= -1
                    case "sticky":
                        self.velocity.x = 0
                        self.velocity.y = 0
                    case "solid":
                        self.velocity.x = 0
            if feety.collide_rect(wall["rect"]) == True:
                match wall["collision_type"]:
                    case "bouncy":
                        self.velocity.y *= -1
                    case "sticky":
                        self.velocity.x = 0
                        self.velocity.y = 0
                    case "solid":
                        self.velocity.y = 0

        self.position += self.velocity.scale(dt)
        self.hitbox.set_center(self.position)
        self.rect.center = (self.hitbox.x+10, self.hitbox.y-6)

        # Teleport the player if he collide with a portal
        for portal in load.get_portals():
            if self.hitbox.collide_rect(load.get_portals()[portal]["rect"]) == True:
                self.position.x, self.position.y = load.get_portal_exit(load.get_portals()[portal]).x, load.get_portal_exit(load.get_portals()[portal]).y
                self.map_name, self.scene_name = load.get_portals()[portal]["targeted_map_name"], load.get_portals()[portal]["targeted_scene_name"]
                entity_handler.need_update = True

class saveEntity:
    def __init__(self, id:int=None):
        self.id:int = id
        self.data:dict = {}

    def load(self, id:int):
        try:
            self.data = save.get("entities")[id]
            return True
        except KeyError:
            self.data = {}
            return False

    def unload(self):
        try:
            entity_handler.entities[self.id] = self.data
            return True
        except KeyError:
            warn("Can't unload entity n°"+str(self.id)+".")
            return False

    def get(self, parameter:str):
        try:
            return self.data[parameter]
        except KeyError:
            return None

    def set(self, parameter:str, value:any):
        try:
            self.data[parameter] = value
            return True
        except KeyError:
            warn("Can't set parameter '"+str(parameter)+"' in entity n°"+str(self.id)+".")
            return False