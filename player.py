import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/knight.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(topleft = pos)
        self.movement_direction = pygame.math.Vector2() #  creates a vector with x and y values

    def input_listener(self):
        #  all keys are detected
        input = pygame.key.get_pressed()
        
        #  in case the player pressed both directions at the same time
        if input[pygame.K_w] and input[pygame.K_s]:
            self.movement_direction.y = 0
        #  if the w/s keys are being pressed manipulate the direction vector we created earlier
        elif input[pygame.K_w]:
            self.movement_direction.y = -1
        elif input[pygame.K_s]:
            self.movement_direction.y = 1
        #  otherwise reset to 0 (other wise the player would move infinitely)
        else:
             self.movement_direction.y = 0

        if input[pygame.K_a] and input[pygame.K_d]:
            self.movement_direction.x = 0
        elif input[pygame.K_a]:
            self.movement_direction.x = -1
        elif input[pygame.K_d]:
            self.movement_direction.x = 1
        else:
            self.movement_direction.x = 0

    def move(self, speed):
        self.rect.topleft += self.movement_direction * speed

    def update(self):
        self.input_listener()
        self.move(3)