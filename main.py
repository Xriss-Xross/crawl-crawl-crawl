import pygame
from scene import Scene


class Game:
    def __init__(self):
        #  boiler plate
        pygame.init()
        self.screen = pygame.display.set_mode((15*48, 15*48))
        pygame.display.set_caption('Crawl Crawl Crawl')
        self.clock = pygame.time.Clock()
        self.scene = Scene(self.screen)


    #  runtime
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.scene.run()
            pygame.display.update()
            self.clock.tick(60)


Game().run()
