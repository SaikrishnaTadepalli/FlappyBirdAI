import pygame

from images import BIRD_IMAGES

class Bird:
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.IMAGES = BIRD_IMAGES
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height  = self.y
        self.image_count = 0
        self.image = self.IMAGES[0]

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # Physics Formula
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        if (displacement >= 16):
            displacement = 16
        
        if (displacement < 0):
            displacement -= 2
        
        self.y = self.y + displacement

        if (displacement < 0) or (self.y < self.height + 50):
            if (self.tilt < self.MAX_ROTATION):
                self.tilt = self.MAX_ROTATION
        else:
            if (self.tilt > -90):
                self.tilt -= self.ROTATION_VELOCITY
    
    def draw(self, win):
        self.image_count += 1

        if (self.image_count < self.ANIMATION_TIME):
            self.image = self.IMAGES[0]
        elif (self.image_count < self.ANIMATION_TIME * 2):
            self.image = self.IMAGES[1]
        elif (self.image_count < self.ANIMATION_TIME * 3):
            self.image = self.IMAGES[2]
        elif (self.image_count < self.ANIMATION_TIME * 4):
            self.image = self.IMAGES[1]
        elif (self.image_count == self.ANIMATION_TIME * 4 + 1):
            self.image = self.IMAGES[0]
            self.image_count = 0
        
        if (self.tilt <= -80):
            self.img = self.IMAGES[1]
            self.image_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.image.get_rect(topleft = (self.x, self.y)).center)

        win.blit(rotated_image, new_rectangle.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.image)