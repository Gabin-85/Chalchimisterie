import pygame
from utils.timeToolbox import Timer
from utils.storageHandler import param_get

class EntityAnimation:

    def __init__(self, entity_name, size, update_time):
        self.current_frame = -1
        self.current_animation = "idle"
        
        self.size = size

        self.sprite_sheet = pygame.image.load("assets/sprites/"+param_get(entity_name, "animation")["sprite_sheet"])
        self.images = self.load_images(param_get(entity_name, "animation")["animations"])

        self.update_time = update_time
        self.timer = Timer(self.update_time)

        self.reset_to("down")

    def load_images(self, dict):
        images = {}
        for event in dict:
            images[event] = {}
            for frame in range(len(dict[event])):
                images[event][frame] = (dict[event][frame]["x"]*self.size[0], dict[event][frame]["y"]*self.size[1], self.size[0], self.size[1])
        return images
    
    def reset_to(self, animation_name):
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.current_frame = -1
            self.timer.reset(self.update_time)    

    def next(self):
        if self.timer.check() or self.current_frame == -1:
            self.current_frame = (self.current_frame + 1) % len(self.images[self.current_animation])
            self.current_image = pygame.Surface(self.size)
            self.current_image.blit(self.sprite_sheet, (0, 0), self.images[self.current_animation][self.current_frame])
            self.current_image.set_colorkey((0, 0, 0))
        return self.current_image.get_rect()