import pygame
from wall import Wall
from floor import Floor
from levels import ROOM5

class Scene:
    def __init__(self, screen):
        
        self.screen = screen
        #  sprite groups (either they are characters or they are environmental obstacles)
        #  sprite groups will be passed into a class as a list becuase sprites can have more than one
        self.sprites = pygame.sprite.Group()
        self.obstruction = pygame.sprite.Group()
        self.environment = pygame.sprite.Group()

        self.generate()

    #  makes a grid from a room
    def generate(self):
        for y, row in enumerate(ROOM5):
            y *= 48
            for x, col in enumerate(row):
                x *= 48
                if col == 'W':
                    Wall((x, y), [self.obstruction])
                else:
                    Floor((x, y), [self.environment])


    def run(self):
        self.obstruction.draw(self.screen)
        self.environment.draw(self.screen)