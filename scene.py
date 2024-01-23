import pygame
from wall import Wall
from floor import Floor
from player import Player
from spawn_enemy import Enemy
from levels import ROOMS

from ui import UI

positions = [(336, 0), (672, 336), (336, 672), (0, 336)]

start = (336, 624)
top = (336, 0)
right = (672, 336)
bottom = (336, 672)
left = (0, 336)


class Scene:
    def __init__(self, screen, level):
        self.screen = screen
        #  sprite groups (whether they are interactable and/or visible etc.)
        #  sprite groups will be passed into a class as a list becuase sprites can have more than one
        self.sprite = pygame.sprite.Group()
        self.obstruction = pygame.sprite.Group()
        self.environment = pygame.sprite.Group()
        self.entity = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.level = level

        self.generate()
        self.ui = UI()


    #  makes a numerical grid from an array
    def generate(self):
        self.enemies_spawned = 0
        to_spawn = []
        for i in range(len(ROOMS[self.level])):
            y = i*48
            for j in range(len(ROOMS[self.level][i])):
                x = j*48
                if ROOMS[self.level][i][j] == 'W':
                    Wall((x, y), [self.obstruction, self.sprite])
                else:
                    Floor((x, y), [self.environment, self.sprite])
                if ROOMS[self.level][i][j] == 'S':
                    to_spawn.append([(x, y), 'slime'])
                elif ROOMS[self.level][i][j] == 'Z':
                    to_spawn.append([(x, y), 'zombie'])
                elif ROOMS[self.level][i][j] == 'K':
                    to_spawn.append([(x, y), 'skeleton'])
                elif ROOMS[self.level][i][j] == 'B':
                    to_spawn.append([(x, y), 'vampire'])

        self.player = Player(positions[0], [self.sprite], self.obstruction)

        for i in to_spawn:
            self.enemies_spawned += 1
            self.enemy = (Enemy(i[0], [self.sprite, self.enemies], i[1], self.obstruction))


    def run(self):
        self.time = pygame.time.get_ticks()
        self.sprite.draw(self.screen)
        self.sprite.update(self.player, self.enemy)
        self.ui.show(self.player.health, self.player.shield, self.time)