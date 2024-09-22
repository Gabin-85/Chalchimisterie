from utils.resourcesHandler import storage, save
from utils.mathToolbox import Vector2D, Vector3D, Rect2D, Rect3D
from utils.entityHandler import entity_handler
from utils.timeToolbox import Timer
from utils.consoleSystem import warn
import pygame, math

class Entity(pygame.sprite.Sprite):

    def __init__ (self) -> None:
        super().__init__()

    def create(self, name, pattern:str, scene_name, map_name, position:Vector2D):
        template = storage.get(pattern, "entities")

        # General data (should not be changed) is the base data of the entity
        self.general_data = {
        "id":len(entity_handler.entities)-1,
        "name":name,
        "pattern":pattern,
        "scene_name":scene_name,
        "map_name":map_name,
        "position":position}

        self.rect = pygame.Rect(0, 0, 0, 0)

        # Flags and data are additionnal activators and values that can be added to the entity
        self.flags = template["flags"]
        self.fdata = template["fdata"]
        # Sdata and Udata is the actual values of the entity (U for unpacked and P for packed)
        self.data = {}
        self.obj_data = {}
        
        # Flag move_self
        if "move_self" in self.flags:

            if "velocity" in self.fdata:
                self.obj_data["velocity"] = Vector2D(self.fdata["velocity"][0], self.fdata["velocity"][1])
            else:
                self.obj_data["velocity"] = Vector2D(0, 0)

            if "mass" in self.fdata:
                self.data["mass"] = self.fdata["mass"]
            else:
                self.data["mass"] = 1

            if "friction" in self.fdata:
                self.data["friction"] = self.fdata["friction"]
            else:
                self.data["friction"] = 0.2

            if "acceleration" in self.fdata:
                self.obj_data["acceleration"] = Vector2D(self.fdata["acceleration"][0], self.fdata["acceleration"][1])
            else:
                self.obj_data["acceleration"] = Vector2D(0, 0)

            if "force" in self.fdata:
                self.data["force"] = self.fdata["force"]
            else:
                self.data["force"] = self.data["mass"]

        # Flag move_him
        elif "move_him" in self.flags:

            if "velocity" in self.fdata:
                self.obj_data["velocity"] = Vector2D(self.fdata["velocity"][0], self.fdata["velocity"][1])
            else:
                self.obj_data["velocity"] = Vector2D(0, 0)

            if "mass" in self.fdata:
                self.data["mass"] = self.fdata["mass"]
            else:
                self.data["mass"] = 1

            if "friction" in self.fdata:
                self.data["friction"] = self.fdata["friction"]
            else:
                self.data["friction"] = 0.2

        # Flag rect_hit
        if "rect_hit" in self.flags:

            if "hitbox" in self.fdata:
                self.obj_data["hitbox"] = Rect2D(self.fdata["hitbox"][0]+self.general_data["position"].x, self.fdata["hitbox"][1]+self.general_data["position"].y, self.fdata["hitbox"][2], self.fdata["hitbox"][3])
            else:
                self.obj_data["hitbox"] = Rect2D(0, 0, 0, 0)

        # Flag rect_hurt
        if "rect_hurt" in self.flags:

            if "hurtbox" in self.fdata:
                self.obj_data["hurtbox"] = Rect2D(self.fdata["hurtbox"][0]+self.general_data["position"].x, self.fdata["hurtbox"][1]+self.general_data["position"].y, self.fdata["hurtbox"][2], self.fdata["hurtbox"][3])
            elif "hitbox" in self.data:
                self.obj_data["hurtbox"] = self.data["hitbox"].__copy__()
            else:
                self.obj_data["hurtbox"] = Rect2D(0, 0, 0, 0)
        
        # Flag display_anim
        if "display_anim" in self.flags:

            if "anim_name" in self.fdata:
                self.data["anim_name"] = self.fdata["anim_name"]
            else:
                self.data["anim_name"] = self.general_data["pattern"]

            if "anim_data" in self.fdata:
                self.data["anim_data"] = self.fdata["anim_data"]
            else:
                self.data["anim_data"] = storage.get(self.data["anim_name"], "animations")

            if "image" in self.fdata:
                self.data["image"] = "assets/sprites/" + self.fdata["image"]
            else:
                self.data["image"] = "assets/sprites/" + self.data["anim_data"]["file"]

            if "anim_default" in self.fdata:
                self.data["anim_animation"] = self.fdata["anim_default"]
                self.data["anim_target_animation"] = self.fdata["anim_default"]
                self.data["anim_frame"] = 0
            else:
                self.data["anim_animation"] = {"direction": None, "action": None}
                self.data["anim_target_animation"] = {"direction": None, "action": None}


            if "anim_timer" in self.fdata:
                self.obj_data["anim_timer"] = Timer(self.fdata["anim_timer"])
            else:
                self.obj_data["anim_timer"] = Timer(0)

            self.texture = pygame.image.load(self.data["image"])

        # Flag display_show
        elif "display_show" in self.flags:
            if "image" in self.fdata:
                self.data["image"] = "assets/sprites/" + self.fdata["image"]
            else:
                # TODO: Default texture
                pass
            self.texture = pygame.image.load(self.data["image"])

    def load(self, id:int):
        # Get the save
        self.save = saveEntity(id)
        self.save.load(id)

        # Set the general data
        self.general_data = self.save.get("general_data")
        self.general_data["position"] = Vector2D(self.general_data["position"][0], self.general_data["position"][1])

        self.rect = pygame.Rect(0, 0, 0, 0)
        
        # Set the flags
        self.flags = self.save.get("flags")
        self.data = self.save.get("data")
        self.obj_data = self.save.get("obj_data")

        # Repack obj_data
        for data in self.obj_data:
            match(self.obj_data[data]["type"]):
                case "Rect2D":
                    self.obj_data[data] = Rect2D(self.obj_data[data]["data"][0], self.obj_data[data]["data"][1], self.obj_data[data]["data"][2], self.obj_data[data]["data"][3])
                case "Rect3D":
                    self.obj_data[data] = Rect3D(self.obj_data[data]["data"][0], self.obj_data[data]["data"][1], self.obj_data[data]["data"][2], self.obj_data[data]["data"][3], self.obj_data[data]["data"][4], self.obj_data[data]["data"][5])
                case "Vector2D":
                    self.obj_data[data] = Vector2D(self.obj_data[data]["data"][0], self.obj_data[data]["data"][1])
                case "Vector3D":
                    self.obj_data[data] = Vector3D(self.obj_data[data]["data"][0], self.obj_data[data]["data"][1], self.obj_data[data]["data"][2])
                case "Timer":
                    self.obj_data[data] = Timer(self.obj_data[data]["data"][0])

        # Data or obj_data that are not saved (for space savings or possibility)
        if "display_anim" in self.flags or "display_show" in self.flags:
            self.texture = pygame.image.load(self.data["image"])
        if "display_anim" in self.flags:
            self.data["anim_data"] = storage.get(self.data["anim_name"], "animations")
            

    def unload(self):
        self.save = saveEntity(self.general_data["id"])

        # Flag savable
        if "savable" in self.flags:

            # General data
            self.general_data["position"] = [self.general_data["position"].x, self.general_data["position"].y]
            self.save.set("general_data", self.general_data)

            # Flags
            self.save.set("flags", self.flags)

            # Data
            if "anim_data" in self.data:
                del self.data["anim_data"]
            self.save.set("data", self.data)

            # Unpack obj_data
            for data in self.obj_data:
                match(self.obj_data[data].__type__()):
                    case "Rect2D":
                        self.obj_data[data] = {"data":[self.obj_data[data].x, self.obj_data[data].y, self.obj_data[data].width, self.obj_data[data].height], "type":"Rect2D"}
                    case "Rect3D":
                        self.obj_data[data] = {"data":[self.obj_data[data].x, self.obj_data[data].y, self.obj_data[data].z, self.obj_data[data].width, self.obj_data[data].height, self.obj_data[data].depth], "type":"Rect3D"}
                    case "Vector2D":
                        self.obj_data[data] = {"data":[self.obj_data[data].x, self.obj_data[data].y], "type":"Vector2D"}
                    case "Vector3D":
                        self.obj_data[data] = {"data":[self.obj_data[data].x, self.obj_data[data].y, self.obj_data[data].z], "type":"Vector3D"}
                    case "Timer":
                        self.obj_data[data] = {"data":[self.obj_data[data].remaining_time()], "type":"Timer"}
            self.save.set("obj_data", self.obj_data)

        else:
            self.save.data = {}

        self.save.unload()

    def physics(self, dt:float):
        from utils.loadHandler import load

        if "move_him" in self.flags or "move_self" in self.flags:
            if "move_self" in self.flags:
                try:
                    self.obj_data["acceleration"].iscale(self.data["force"]/self.data["mass"])
                except ValueError:
                    self.obj_data["acceleration"] = Vector2D(0, 0)
                self.obj_data["velocity"] -= (self.obj_data["velocity"].scale(self.data["friction"] / self.data["mass"]) - self.obj_data["acceleration"]).scale(dt)
            else:
                self.obj_data["velocity"] -= (self.obj_data["velocity"].scale(self.data["friction"] / self.data["mass"]))

            if "rect_hit" in self.flags:
                feetx:Rect2D = self.obj_data["hitbox"]+Vector2D(self.obj_data["velocity"].x, 0)
                feety:Rect2D = self.obj_data["hitbox"]+Vector2D(0, self.obj_data["velocity"].y)

                if "walls_collide" in self.flags:
                    for wall in load.get_walls():
                        if feetx.collide_rect(wall["rect"]) == True:
                            match wall["collision_type"]:
                                case "bouncy":
                                    self.obj_data["velocity"].x *= -1
                                case "sticky":
                                    self.obj_data["velocity"].x = 0
                                    self.obj_data["velocity"].y = 0
                                case "solid":
                                    self.obj_data["velocity"].x = 0
                        if feety.collide_rect(wall["rect"]) == True:
                            match wall["collision_type"]:
                                case "bouncy":
                                    self.obj_data["velocity"].y *= -1
                                case "sticky":
                                    self.obj_data["velocity"].x = 0
                                    self.obj_data["velocity"].y = 0
                                case "solid":
                                    self.obj_data["velocity"].y = 0
                
                if "portals_block" in self.flags:
                    for portal in load.get_portals():
                        if feetx.collide_rect(load.get_portals()[portal]["rect"]) == True:
                            self.obj_data["velocity"].x = 0
                        if feety.collide_rect(load.get_portals()[portal]["rect"]) == True:
                            self.obj_data["velocity"].y = 0

                if "entities_collide" in self.flags:
                    for entity in entity_handler.get_entities():
                        if "hitbox" in entity.obj_data and self.general_data["id"] != entity.general_data["id"]:
                            if self.obj_data["hitbox"].collide_rect(entity.obj_data["hitbox"]) == True:
                                self.obj_data["velocity"] += Vector2D(self.obj_data["hitbox"].x - entity.obj_data["hitbox"].x, self.obj_data["hitbox"].y - entity.obj_data["hitbox"].y).normalize().scale(0.1)
                                entity.obj_data["velocity"] -= Vector2D(self.obj_data["hitbox"].x - entity.obj_data["hitbox"].x, self.obj_data["hitbox"].y - entity.obj_data["hitbox"].y).normalize().scale(0.1)
                            if feetx.collide_rect(entity.obj_data["hitbox"]) == True:
                                temp_entity_velocity, temp_self_velocity = (self.data["mass"]/ entity.data["mass"]) * (self.obj_data["velocity"].x - entity.obj_data["velocity"].x), (entity.data["mass"]/ self.data["mass"]) * (self.obj_data["velocity"].x - entity.obj_data["velocity"].x)
                                self.obj_data["velocity"].x -= temp_self_velocity
                                entity.obj_data["velocity"].x += temp_entity_velocity
                            if feety.collide_rect(entity.obj_data["hitbox"]) == True:
                                temp_entity_velocity, temp_self_velocity = (self.data["mass"]/ entity.data["mass"]) * (self.obj_data["velocity"].y - entity.obj_data["velocity"].y), (entity.data["mass"]/ self.data["mass"]) * (self.obj_data["velocity"].y - entity.obj_data["velocity"].y)
                                self.obj_data["velocity"].y -= temp_self_velocity
                                entity.obj_data["velocity"].y += temp_entity_velocity  

            # Need update all physics position and rects
            self.general_data["position"] += self.obj_data["velocity"].scale(dt)
            if "rect_hit" in self.flags:
                self.obj_data["hitbox"] += self.obj_data["velocity"].scale(dt)
            if "rect_hurt" in self.flags:
                self.obj_data["hurtbox"] += self.obj_data["velocity"].scale(dt)
        # Here we math.floor() because otherwise the player will be visualy stuck in the wall (It does not affect the physics)
        self.rect.center = (math.floor(self.general_data["position"].x), math.floor(self.general_data["position"].y))

        if "portals_pass" in self.flags and "rect_hit" in self.flags:
            # Teleport the player if he collide with a portal
            for portal in load.get_portals():
                if self.obj_data["hitbox"].collide_rect(load.get_portals()[portal]["rect"]) == True:
                    # Need update all physics position and rects
                    temp = Vector2D(load.get_portal_exit(load.get_portals()[portal]).x-self.general_data["position"].x, load.get_portal_exit(load.get_portals()[portal]).y-self.general_data["position"].y)
                    self.general_data["position"] += temp
                    self.obj_data["hitbox"] += temp
                    if "rect_hurt" in self.flags:
                        self.obj_data["hurtbox"] += temp
                    self.general_data["map_name"], self.general_data["scene_name"] = load.get_portals()[portal]["targeted_map_name"], load.get_portals()[portal]["targeted_scene_name"]
                    entity_handler.need_update = True

    def render(self):
        if "display_anim" in self.flags:

            # To verify if the surface need an update
            anim_update = False

            if self.data["anim_target_animation"]["action"] != self.data["anim_animation"]["action"] or self.data["anim_target_animation"]["direction"] != self.data["anim_animation"]["direction"]:
                # Change the animation and the frame
                self.data["anim_animation"] = self.data["anim_target_animation"].copy()
                self.data["anim_frame"] = 0
                self.obj_data["anim_timer"].reset(self.data["anim_data"]["frames"][self.data["anim_data"]["anim"][self.data["anim_animation"]["action"]]["from"]]["duration"])
                anim_update = True
            elif self.obj_data["anim_timer"].check():
                # Change the frame
                self.data["anim_frame"] = (self.data["anim_frame"]+1)%(self.data["anim_data"]["anim"][self.data["anim_animation"]["action"]]["to"]-self.data["anim_data"]["anim"][self.data["anim_animation"]["action"]]["from"]+1)
                self.obj_data["anim_timer"].reset(self.data["anim_data"]["frames"][self.data["anim_frame"]+self.data["anim_data"]["anim"][self.data["anim_animation"]["action"]]["from"]]["duration"])
                anim_update = True

            if anim_update == True:

                # Create the image (it's a surface DON'T RENAME IT)
                self.image = pygame.Surface((self.data["anim_data"]["frames"][self.data["anim_frame"]+self.data["anim_data"]["anim"][self.data["anim_animation"]["action"]]["from"]]["frame"]["w"],
                                                self.data["anim_data"]["frames"][self.data["anim_frame"]+self.data["anim_data"]["anim"][self.data["anim_animation"]["action"]]["from"]]["frame"]["h"]))

                # Crop the imag into the surface
                self.image.blit(self.texture, (0, 0),
                    (self.data["anim_data"]["frames"][self.data["anim_frame"]+self.data["anim_data"]["anim"][self.data["anim_animation"]["action"]]["from"]]["frame"]["x"],
                    self.data["anim_data"]["frames"][self.data["anim_frame"]+self.data["anim_data"]["anim"][self.data["anim_animation"]["action"]]["from"]]["frame"]["y"],
                    self.data["anim_data"]["frames"][self.data["anim_frame"]+self.data["anim_data"]["anim"][self.data["anim_animation"]["action"]]["from"]]["frame"]["w"],
                    self.data["anim_data"]["frames"][self.data["anim_frame"]+self.data["anim_data"]["anim"][self.data["anim_animation"]["action"]]["from"]]["frame"]["h"]))
                
                # Flip it if needed
                if self.data["anim_animation"]["direction"] == "right":
                    self.image = pygame.transform.flip(self.image, True, False)

                # Set the colorkey (to black) and set the rect
                self.image.set_colorkey((0, 0, 0))

                # Set the rect (DON'T RENAME IT)
                self.rect = self.image.get_rect()

        elif "display_show" in self.flags:
            self.image = pygame.Surface(self.texture.get_size())
            self.image.blit(self.texture, (0, 0))
            self.image.set_colorkey((0, 0, 0))
            rect = self.image.get_rect()
            rect.x, rect.y = self.rect.x, self.rect.y
            self.rect = rect


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