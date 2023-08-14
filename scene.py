import pygame
from tile import Tile
from levels import ROOM1

class Scene:
    def __init__(self, screen):
        
        self.screen = screen
        #  sprite groups (either they are characters or they are environmental obstacles)
        self.sprites = pygame.sprite.Group()
        self.environment = pygame.sprite.Group()

        self.generate()

    #  makes a grid from a room
    def generate(self):
        for y, row in enumerate(ROOM1):
            y *= 48
            for x, col in enumerate(row):
                x *= 48
                if col == 'W':
                    Tile((x, y), [self.environment])


    def run(self):
        self.environment.draw(self.screen)