import pygame
from wall import Wall
from floor import Floor
from player import Player
from levels import ROOM1
from ui import UI

top = (336, 0)
right = (672, 336)
bottom = (336, 672)
left = (0, 336)

class Scene:
    def __init__(self, screen):
        
        self.screen = screen
        #  sprite groups (whether they are interactable and/or visible etc.)
        #  sprite groups will be passed into a class as a list becuase sprites can have more than one
        self.sprite = pygame.sprite.Group()
        self.obstruction = pygame.sprite.Group()
        self.environment = pygame.sprite.Group()
        self.entity = pygame.sprite.Group()

        self.generate()
        self.ui = UI()

    #  makes a numerical grid from an array
    def generate(self):
        for y, row in enumerate(ROOM1):
            y *= 48
            for x, col in enumerate(row):
                x *= 48
                if col == 'W':
                    Wall((x, y), [self.obstruction, self.sprite])
                else:
                    Floor((x, y), [self.environment, self.sprite])
        self.player = Player(bottom, [self.sprite], self.obstruction)


    def run(self):
        self.sprite.draw(self.screen)
        self.sprite.update()
        self.ui.show(self.player.health, self.player.shield, self.player.xp)