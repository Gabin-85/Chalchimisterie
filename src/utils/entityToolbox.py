from utils.resourcesHandler import storage
from utils.saveHandler import saveEntity, save
from utils.timeToolbox import Timer
from utils.loadHandler import scene
import pygame
import math

class Entity(pygame.sprite.Sprite):

    def __init__ (self) -> None:
        super().__init__()
        self.name = None
        self.id = None
        self.save = None

    def create(self, name:str):
        template = storage.get(name, "entity")

        # General
        self.id = len(save.loaded_files[save.selected_save]["entity"])
        self.name = name
        self.rect = pygame.Rect(0, 0, 0, 0)

        # Position
        self.scene_name:str = template["scene_name"]
        self.map_name:str = template["map_name"]
        self.position:pygame.Vector2 = pygame.Vector2(*template["position"])

        # Boxes
        self.hitbox:pygame.Rect = pygame.Rect(*template["hitbox"])
        self.hurtbox:pygame.Rect = pygame.Rect(*template["hurtbox"])

        # Physics
        self.velocity:pygame.Vector2 = pygame.Vector2(*template["velocity"])
        self.acceleration:pygame.Vector2 = pygame.Vector2(0, 0)
        self.mass:float = template["mass"]
        self.force:float = template["force"]
        self.friction:float = template["friction"]

        # Textures and animation
        self.texture:dict = storage.get(self.name, "animations")
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
        self.save:saveEntity = saveEntity(id)
        self.save.load()

        # General
        self.id = id
        self.name = self.save.get("name")
        self.rect = pygame.Rect(0, 0, 0, 0)

        # Position
        self.scene_name:str = self.save.get("scene_name")
        self.map_name:str = self.save.get("map_name")
        self.position:pygame.Vector2 = pygame.Vector2(self.save.get("position"))

        # Boxes
        self.hitbox:pygame.Rect = pygame.Rect(*self.save.get("hitbox"))
        self.hurtbox:pygame.Rect = pygame.Rect(*self.save.get("hurtbox"))

        # Physics
        self.velocity:pygame.Vector2 = pygame.Vector2(*self.save.get("velocity"))
        self.acceleration:pygame.Vector2 = pygame.Vector2(0, 0)
        self.mass:float = self.save.get("mass")
        self.force:float = self.save.get("force")
        self.friction:float = self.save.get("friction")

        # Textures and animation
        self.texture:dict = storage.get(self.name, "animations")
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
        self.save:saveEntity = saveEntity(self.id)
        self.save.create()

        # General
        self.save.set("name", self.name)

        # Position
        self.save.set("scene_name", self.scene_name)
        self.save.set("map_name", self.map_name)
        self.save.set("position", [self.position.x, self.position.y])

        # Boxes
        self.save.set("hitbox", [self.hitbox.x, self.hitbox.y, self.hitbox.w, self.hitbox.h])
        self.save.set("hurtbox", [self.hurtbox.x, self.hurtbox.y, self.hurtbox.w, self.hurtbox.h])

        # Physics
        self.save.set("velocity", [self.velocity.x, self.velocity.y])
        self.save.set("mass", self.mass)
        self.save.set("force", self.force)
        self.save.set("friction", self.friction)

        # Animation
        self.save.set("animation", self.animation)
        self.save.set("animation_frame", self.animation_frame)
        self.save.set("animation_timer", self.animation_timer.remaining_time())

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

    def update(self, dt):
        try:
            self.acceleration.scale_to_length(self.force/self.mass)
        except ValueError:
            self.acceleration = pygame.Vector2(0, 0)
        self.velocity -= self.velocity * self.friction / self.mass - self.acceleration

        marging = pygame.Vector2(0, 0)
        if self.velocity.x > 0:
            marging.x = math.ceil(self.velocity.x)
        else:
            marging.x = math.floor(self.velocity.x)
        if self.velocity.y > 0:
            marging.y = math.ceil(self.velocity.y)
        else:
            marging.y = math.floor(self.velocity.y)
        feetx = pygame.Rect(self.hitbox.x + marging.x, self.hitbox.y, self.hitbox.width, self.hitbox.height)
        feety = pygame.Rect(self.hitbox.x, self.hitbox.y + marging.y, self.hitbox.width, self.hitbox.height)

        # TODO: Modify the player move part so we can separate x and y
        for wall in scene.get_walls():
            if feetx.colliderect(wall["rect"]) == True:
                match wall["collision_type"]:
                    case "bouncy":
                        self.velocity.x *= -1
                    case "sticky":
                        self.velocity.x = 0
                        self.velocity.y = 0
                    case "solid":
                        self.velocity.x = 0
            if feety.colliderect(wall["rect"]) == True:
                match wall["collision_type"]:
                    case "bouncy":
                        self.velocity.y *= -1
                    case "sticky":
                        self.velocity.x = 0
                        self.velocity.y = 0
                    case "solid":
                        self.velocity.y = 0

        self.position += self.velocity*dt
        self.hitbox.center = self.position
        self.rect.center = (self.hitbox.x+10, self.hitbox.y-6)

        # Teleport the player if he collide with a portal
        for portal in scene.get_portals():
            if self.hitbox.colliderect(scene.get_portals()[portal]["rect"]) == True:
                self.position.x, self.position.y = scene.get_portal_exit(scene.get_portals()[portal]).x, scene.get_portal_exit(scene.get_portals()[portal]).y
                self.map_name, self.scene_name = scene.get_portals()[portal]["targeted_map_name"], scene.get_portals()[portal]["targeted_scene_name"]