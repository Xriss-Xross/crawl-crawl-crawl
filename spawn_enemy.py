import pygame
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, enemy):
        super().__init__(groups)
        self.enemy_folder = f'./assets/{enemy}/'
        self.frame = 0
        self.movement_direction = pygame.math.Vector2()
        self.sprite_type = enemy
        self.image = pygame.image.load(self.enemy_folder+f'{enemy}1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))        
        self.rect = self.image.get_rect(topleft = pos)
       

        self.asset_loader()


    def asset_loader(self):
        
        self.enemy_frames = []

        def import_images(path):
            images = []
            for image in os.listdir(path):
                image_surf = pygame.image.load(path + image).convert_alpha()
                images.append(image_surf)
            return images


        self.enemy_frames = import_images(self.enemy_folder)


    def move(self):
        #  if you move diagonally you gain speed which although is something that is weird
        #  I think its a pretty funny feature that will aid in speedrunning for players
        self.rect.x += self.movement_direction.x * self.speed
        self.collide('x')
        self.rect.y += self.movement_direction.y * self.speed
        self.collide('y')


    def animate(self): 
        self.frame += 0.025
        self.animation = self.enemy_frames
        if self.frame >= len(self.animation):
            self.frame = 0
        self.image = self.animation[int(self.frame)]
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center = self.rect.center)   


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
        self.animate()