import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstruction):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/knight/idle_left/knight1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
        self.attack_query = False
        self.attacking = False

        self.obstruction = obstruction
        self.movement_direction = pygame.math.Vector2() #  creates a vector with x and y values


        self.attack_cooldown = 20
        self.cooldown = 20

        self.state = 'idle_right'
        self.asset_loader()


    def asset_loader(self):
        knight_folder = 'C:/Users/killi/code/python/crawl-crawl-crawl/assets/knight/'
        self.knight_states = {'left': [], 'right': [], 'attack_left': [], 'attack_right': [], 'idle_left': [], 'idle_right': []}

        def import_images(path):
            images = []
            for image in os.listdir(path):
                image_surf = pygame.image.load(path + image).convert_alpha()
                images.append(image_surf)
            return images

        for state in self.knight_states.keys():
            path = knight_folder + state + '/'

            self.knight_states[state] = import_images(path)


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
            self.state = 'left'
        elif input[pygame.K_d]:
            self.movement_direction.x = 1
            self.state = 'right'
        else:
            self.movement_direction.x = 0

        #  attack input
        if input[pygame.K_SPACE] and self.attack_cooldown == self.cooldown:
            self.attack_cooldown = 0
            self.attack_query = True
            if 'idle_' in self.state:
                self.state = self.state.replace('idle_', 'attack_')
            elif 'attack_' not in self.state:
                self.state = 'attack_' + self.state


    def idle_listener(self):
        if 'attack_' in self.state:
            if self.attack_query == True:
                self.attack_query = False
                self.state = self.state[7:]
    
        if self.movement_direction.x == 0 and self.movement_direction.y == 0 and 'idle_' not in self.state and 'attack_' not in self.state:
            self.state = 'idle_' + self.state


    def animate(self): 
        if 'attack_' in self.state or self.attacking == True:
            if self.attacking != True:
                self.frame = 0
                self.animation = self.knight_states[self.state]
            self.frame += 0.15
            self.attacking = True
            self.image = self.animation[int(self.frame)]
            if int(self.frame) == 3:
                self.attacking = False


        elif self.attacking == False:
            self.frame += 0.15
            self.animation = self.knight_states[self.state]
            if self.frame >= len(self.animation):
                self.frame = 0
            self.image = self.animation[int(self.frame)]
            self.rect = self.image.get_rect(center = self.rect.center)   


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
        self.animate()
        self.idle_listener()
        self.move(3)