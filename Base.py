import pygame

from images import BASE_IMAGE

class Base:
    VELOCITY = 5
    WIDTH = BASE_IMAGE.get_width()
    IMAGE = BASE_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if (self.x1 + self.WIDTH < 0):
            self.x1 = self.x2 + self.WIDTH
        
        if (self.x2 + self.WIDTH < 0):
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, win):
        win.blit(self.IMAGE, (self.x1, self.y))
        win.blit(self.IMAGE, (self.x2, self.y))