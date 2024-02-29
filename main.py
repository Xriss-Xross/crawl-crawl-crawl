import pygame
from scene import Scene
from game_generation import generate
from database import db_utils


class Game:
    def __init__(self, charID):
        db = db_utils()
        #  boiler plate
        pygame.init()
        self.screen = pygame.display.set_mode((15*48, 15*48), pygame.NOFRAME)
        pygame.display.set_caption('Crawl Crawl Crawl')
        self.clock = pygame.time.Clock()

        map = db.execute(f"SELECT Map FROM Characters WHERE CharacterID = {charID}").fetchall()[0][0]
        map = eval(map)

        level = map[db.execute(f"SELECT Level FROM Characters WHERE CharacterID = {charID}").fetchall()[0][0]]
        self.scene = Scene(self.screen, level, db, charID)


    #  runtime
    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.scene.run()
            pygame.display.update()
            self.clock.tick(60)


    def quit(self):
        pygame.quit()