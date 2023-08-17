import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstruction):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/knight.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(topleft = pos)

        self.obstruction = obstruction
        self.movement_direction = pygame.math.Vector2() #  creates a vector with x and y values
        self.attack_cooldown = 20
        self.cooldown = 20


    def asset_loader(self):
        pass


    def input_listener(self):
        #  all keys are detected
        input = pygame.key.get_pressed()
        
        #  movement input
        if input[pygame.K_w] and input[pygame.K_s]:
            self.movement_direction.y = 0
        elif input[pygame.K_w]:
            self.movement_direction.y = -1
        elif input[pygame.K_s]:
            self.movement_direction.y = 1
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

        #  attack input
        if input[pygame.K_SPACE] and self.attack_cooldown == self.cooldown:
            print('attack')
            self.attack_cooldown = 0


    def cooldown_handler(self):
        if self.attack_cooldown != self.cooldown:
            self.attack_cooldown += 1
        

    def move(self, speed):
        #  if you move diagonally you gain speed which although is something that is weird
        #  I think its a pretty funny feature that will aid in speedrunning for players
        self.rect.x += self.movement_direction.x * speed
        self.collide('x')
        self.rect.y += self.movement_direction.y * speed
        self.collide('y')


    def collide(self, movement_direction):
        if movement_direction == 'x':
            for obstacle in self.obstruction:
                #  check every single obstacle
                if obstacle.rect.colliderect(self.rect):
                    if self.movement_direction.x > 0: #  player must be moving right
                        self.rect.right = obstacle.rect.left
                    if self.movement_direction.x < 0: #  player must be moving left
                        self.rect.left = obstacle.rect.right
                        
        if movement_direction == 'y':
            for obstacle in self.obstruction:
                if obstacle.rect.colliderect(self.rect):
                    if self.movement_direction.y > 0:
                        self.rect.bottom = obstacle.rect.top
                    if self.movement_direction.y < 0:
                        self.rect.top = obstacle.rect.bottom


    def update(self):
        self.cooldown_handler()
        self.input_listener()
        self.move(3)