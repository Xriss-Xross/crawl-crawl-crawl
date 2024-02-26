import pygame
import sqlite3
import os


enemy_stats = {
    'slime': {'health': 10, 'damage': 2, 'cooldown': 90, 'speed': 2, 'attack_range': 20, 'detection_range': 100},
    'zombie': {'health': 10, 'damage': 3, 'cooldown': 120, 'speed': 1, 'attack_range': 20, 'detection_range': 50},
    'skeleton': {'health': 5, 'damage': 1, 'cooldown': 90, 'speed': 1, 'attack_range': 40, 'detection_range': 100},
    'vampire': {'health': 15, 'damage': 2, 'cooldown': 50, 'speed': 4, 'attack_range': 20, 'detection_range': 800}
}


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, enemy, obstruction, db):
        super().__init__(groups)
        self.db = db
        self.enemy_folder = f'./assets/{enemy}/'
        self.frame = 0
        self.movement_direction = pygame.math.Vector2()
        self.sprite_type = enemy
        self.image = pygame.image.load(self.enemy_folder+f'{enemy}1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.status = 'idle'
        self.obstruction = obstruction

        self.health = enemy_stats[enemy]['health']
        self.damage = enemy_stats[enemy]['damage']
        self.cooldown = enemy_stats[enemy]['cooldown']
        self.speed = enemy_stats[enemy]['speed']
        self.attack_range = enemy_stats[enemy]['attack_range']
        self.detection_range = enemy_stats[enemy]['detection_range']
        
        self.attack_cooldown = self.cooldown

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


    def player_listener(self, player):
        enemy_pos = pygame.math.Vector2(self.rect.center)
        player_pos = pygame.math.Vector2(player.rect.center)

        distance = (player_pos - enemy_pos).magnitude()  # turns the vector into a distance

        if distance > 25:
            direction = (player_pos - enemy_pos).normalize()  # easy normalization
        else:
            direction = pygame.math.Vector2()


        if 'attack_' in player.state:
            if player.rect.colliderect(self.rect):
                self.health -= player.damage

        return(distance, direction)


    def player_reaction(self, player):
        if self.status == 'moving':
            self.movement_direction = self.player_listener(player)[1]
        elif self.status == 'attack':
            if player.shield > self.damage:
                player.shield -= self.damage
            elif player.shield > 0:
                player.shield = 0
            else:
                player.health -= self.damage
        else:
            self.movement_direction = pygame.math.Vector2()


    def move(self):
        self.rect.x += self.movement_direction.x * self.speed
        self.collide('x')
        self.rect.y += self.movement_direction.y * self.speed
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


    def status_listener(self, player, enemy):
        distance = self.player_listener(player)[0]

        if distance <= self.attack_range and self.attack_cooldown == self.cooldown:
            self.status = 'attack'
            self.attack_cooldown = 0
        elif distance <= self.detection_range:
            self.status = 'moving'
        else:
            self.status = 'idle'

        if self.health <= 0:
            if player.shield < player.max_shield:
                player.shield += 1
            self.kill()

            self.db.execute(f"UPDATE Characters SET Enemies_Defeated = Enemies_Defeated + 1 WHERE CharacterID = 1")


    def cooldown_handler(self):
        if self.attack_cooldown != self.cooldown:
            self.attack_cooldown += 1


    def animate(self): 
        self.frame += 0.025
        self.animation = self.enemy_frames
        if self.frame >= len(self.animation):
            self.frame = 0
        self.image = self.animation[int(self.frame)]
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center = self.rect.center)   


    def update(self, player, enemy):
        self.move()
        self.cooldown_handler()
        self.player_listener(player)
        self.status_listener(player, enemy,)
        self.player_reaction(player)
        self.animate()
