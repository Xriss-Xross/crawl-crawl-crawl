import pygame
from scene import Scene
from game_generation import generate


class Game:
    def __init__(self):
        #  boiler plate
        pygame.init()
        self.screen = pygame.display.set_mode((15*48, 15*48), pygame.NOFRAME)
        pygame.display.set_caption('Crawl Crawl Crawl')
        self.clock = pygame.time.Clock()
        levels = generate()
        level = levels[0][0]
        self.scene = Scene(self.screen, level)


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


Game().play()
