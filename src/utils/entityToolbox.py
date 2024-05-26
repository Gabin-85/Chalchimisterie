from utils.resourcesHandler import storage, save
from utils.mathToolbox import Vector2D, Rect2D
from utils.entityHandler import entity_handler
from utils.timeToolbox import Timer
from utils.consoleSystem import warn
import pygame, math

class Entity(pygame.sprite.Sprite):

    def __init__ (self) -> None:
        super().__init__()
        self.name = None
        self.id = None
        self.save = None

    def create(self, name, pattern:str, scene_name, map_name, position:Vector2D):
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
        self.hitbox:Rect2D = Rect2D(self.position.x+template["hitbox"][0], self.position.y+template["hitbox"][1], template["hitbox"][2], template["hitbox"][3])
        self.hurtbox:Rect2D = Rect2D(self.position.x+template["hurtbox"][0], self.position.y+template["hurtbox"][1], template["hurtbox"][2], template["hurtbox"][3])

        # Physics
        self.velocity:Vector2D = Vector2D(*template["velocity"])
        self.acceleration:Vector2D = Vector2D(0, 0)
        self.mass:float = template["mass"]
        self.force:float = template["force"]
        self.friction:float = template["friction"]

        # Textures and animation
        self.animation:dict = storage.get(self.pattern, "animations")
        self.animation_image:pygame.image = pygame.image.load("assets/sprites/" + self.animation["file"])
        self.animation_timer:Timer = Timer(0)
        self.change_animation(template["animation_default"])

    def load(self, id:int):
        # Get the save
        self.save = saveEntity(id)
        self.save.load(id)
        # Get the pattern
        template = storage.get(self.save.get("pattern"), "entities")

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
        self.hitbox:Rect2D = Rect2D(self.position.x+template["hitbox"][0], self.position.y+template["hitbox"][1], template["hitbox"][2], template["hitbox"][3])
        self.hurtbox:Rect2D = Rect2D(self.position.x+template["hurtbox"][0], self.position.y+template["hurtbox"][1], template["hurtbox"][2], template["hurtbox"][3])

        # Physics
        self.velocity:Vector2D = Vector2D(*self.save.get("velocity"))
        self.acceleration:Vector2D = Vector2D(0, 0)
        self.mass:float = self.save.get("mass")
        self.force:float = self.save.get("force")
        self.friction:float = self.save.get("friction")

        # Textures and animation
        self.animation:dict = storage.get(self.pattern, "animations")
        self.animation_image:pygame.image = pygame.image.load("assets/sprites/" + self.animation["file"])
        self.animation_timer:Timer = Timer(self.save.get("animation_timer"))
        self.change_animation(self.save.get("current_animation"))
        self.current_frame = self.save.get("current_frame")

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

        # Physics
        self.save.set("velocity", [self.velocity.x, self.velocity.y])
        self.save.set("mass", self.mass)
        self.save.set("force", self.force)
        self.save.set("friction", self.friction)

        # Animation
        self.save.set("animation_timer", self.animation_timer.remaining_time())
        self.save.set("current_animation", self.current_animation["name"])
        self.save.set("current_frame", self.current_frame)

        self.save.unload()

    def start_animation(self):
        self.animation_timer.start()

    def stop_animation(self):
        self.animation_timer.stop()

    def change_animation(self, animation:str):
        self.current_animation = [obj for obj in self.animation["anim"] if obj["name"] == animation][0]
        self.current_frame = 0

    def change_frame(self) -> pygame.Rect:
        if self.animation_timer.check():

            # Change the animation
            self.current_frame = (self.current_frame+1)%(self.current_animation["to"]-self.current_animation["from"]+1)
            self.animation_timer.reset(self.animation["frames"][self.current_frame+self.current_animation["from"]]["duration"])

            # Change the frame
            self.image = pygame.Surface([self.animation["frames"][self.current_frame+self.current_animation["from"]]["frame"]["w"],
                                         self.animation["frames"][self.current_frame+self.current_animation["from"]]["frame"]["h"]])
            self.image.blit(self.animation_image, (0, 0),
                (self.animation["frames"][self.current_frame+self.current_animation["from"]]["frame"]["x"],
                self.animation["frames"][self.current_frame+self.current_animation["from"]]["frame"]["y"],
                self.animation["frames"][self.current_frame+self.current_animation["from"]]["frame"]["w"],
                self.animation["frames"][self.current_frame+self.current_animation["from"]]["frame"]["h"]))
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()

    def update(self, dt:float):
        try:
            self.acceleration.scale(self.force/self.mass)
        except ValueError:
            self.acceleration = Vector2D(0, 0)
        self.velocity -= (self.velocity.scale(self.friction / self.mass) - self.acceleration).scale(dt)
        feetx = self.hitbox+Vector2D(self.velocity.x, 0)
        feety = self.hitbox+Vector2D(0, self.velocity.y)

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

        # Need update all physics position and rects
        self.position += self.velocity.scale(dt)
        self.hitbox += self.velocity.scale(dt)
        self.hurtbox += self.velocity.scale(dt)
        # Here we math.floor() because otherwise the player will be visualy stuck in the wall (It does not affect the physics)
        self.rect.center = (math.floor(self.position.x), math.floor(self.position.y))

        # Teleport the player if he collide with a portal
        for portal in load.get_portals():
            if self.hitbox.collide_rect(load.get_portals()[portal]["rect"]) == True:
                # Need update all physics position and rects
                temp = Vector2D(load.get_portal_exit(load.get_portals()[portal]).x-self.position.x, load.get_portal_exit(load.get_portals()[portal]).y-self.position.y)
                self.position += temp; self.hitbox += temp; self.hurtbox += temp
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