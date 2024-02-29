import pygame
from game_generation import generate
from menuUI import MenuUI

class Menu:
    def __init__(self):
        #  boiler plate
        pygame.init()
        self.screen = pygame.display.set_mode((15*48, 15*48), pygame.NOFRAME)
        pygame.display.set_caption('Menu')
        self.clock = pygame.time.Clock()
        levels = generate()
        self.scene = MenuUI(levels)

#  runtime
    def play(self): 
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.screen.fill((27, 18, 51))

            self.scene.show()
            pygame.display.update()
            self.clock.tick(60)


    def quit(self):
        pygame.quit()


Menu().play()
