import pygame
import os
from database import db_utils

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstruction, exits, charID):
        super().__init__(groups)
        self.charID = charID
        self.image = pygame.image.load('./assets/knight/idle_left/knight1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(topleft = pos)
        self.frame = 0
        self.attack_query = False
        self.attacking = False

        self.obstruction = obstruction
        self.exits = exits
        self.movement_direction = pygame.math.Vector2() #  creates a vector for x and y values

        #  main player stats
        self.max_health = db_utils().execute(f"SELECT Max_Health FROM Characters WHERE CharacterID = {charID}").fetchall()[0][0]
        self.health = self.max_health

        self.max_shield = db_utils().execute(f"SELECT Max_Shield FROM Characters WHERE CharacterID = {charID}").fetchall()[0][0]
        self.shield = self.max_shield

        self.damage = db_utils().execute(f"SELECT Damage FROM Characters WHERE CharacterID = {charID}").fetchall()[0][0]
        self.speed = db_utils().execute(f"SELECT Speed FROM Characters WHERE CharacterID = {charID}").fetchall()[0][0]
        self.xp = db_utils().execute(f"SELECT XP FROM Characters WHERE CharacterID = {charID}").fetchall()[0][0]

        #  for the cooldown handler later
        self.attack_cooldown = 20
        self.cooldown = 20

        #  default state for the character starting out
        self.state = 'idle_right'
        self.asset_loader()


    def asset_loader(self):
        
        knight_folder = './assets/knight/'
        #  after the function is complete will contain the pygame images of all animated states
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


    def move(self):
        #  player's rectangle (within which the player is drawn) is moved
        self.rect.x += self.movement_direction.x * self.speed

        #  immediately after manipulating the player's position
        #  collisions are checked for
        self.collide('x')
        self.rect.y += self.movement_direction.y * self.speed
        self.collide('y')
        

        if self.rect.y == 0:  # if the player is attempting to leave the room a completion check will be made
            en_s = db_utils().execute(f"SELECT Enemies_Spawned FROM Characters WHERE CharacterID = {self.charID}").fetchall()[0][0]
            en_d = db_utils().execute(f"SELECT Enemies_Defeated FROM Characters WHERE CharacterID = {self.charID}").fetchall()[0][0]
            if en_s == en_d:
                currentLevel = db_utils().execute(f"SELECT Level FROM Characters WHERE CharacterID = {self.charID}").fetchall()[0][0]
                currentTime = db_utils().execute(f"SELECT Time FROM Characters WHERE CharacterID = {self.charID}").fetchall()[0][0]
                if currentLevel != 6:  # if the completion check is complete and there are no more levels the game is done
                    db_utils().execute(f"UPDATE Characters SET Level = {currentLevel + 1}, Time = {currentTime + pygame.time.get_ticks()} WHERE CharacterID = {self.charID}")
                    
                    from main import Game  # to prevent circular import class is only called here
                    pygame.quit()
                    Game(self.charID).play()
                else:  # if there are more rooms to complete
                    time = db_utils().execute(f"SELECT Time FROM Characters WHERE CharacterID = {self.charID}").fetchall()[0][0]
                    db_utils().execute(f"UPDATE Characters SET Final_Time = {time} WHERE CharacterID = {self.charID}")

                    from menu import Menu
                    pygame.quit()
                    Menu().play()


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


    def idle_listener(self):
        #  makes sure that a state can't end up being invalid
        if 'attack_' in self.state:
            if self.attack_query == True:
                self.attack_query = False
                self.state = self.state[7:]
    
        if self.movement_direction.x == 0 and self.movement_direction.y == 0 and 'idle_' not in self.state and 'attack_' not in self.state:
            self.state = 'idle_' + self.state


    def cooldown_handler(self):
        #  a countdown for when the player can next attack
        if self.attack_cooldown != self.cooldown:
            self.attack_cooldown += 1


    def animate(self): 
        #  attack frames are run through
        if 'attack_' in self.state or self.attacking == True:
            if self.attacking != True:
                self.frame = 0
                self.animation = self.knight_states[self.state]
            self.frame += 0.1
            #  frame is rounded to the next int to decide what frame should
            #  be displayed
            self.attacking = True
            self.image = self.animation[int(self.frame)]
            if int(self.frame) == 3:
                self.attacking = False
            #  if the final attack frame is displayed then the attack is over


        elif self.attacking == False:  # otherwise the player is animated normally
            self.frame += 0.15
            self.animation = self.knight_states[self.state]
            if self.frame >= len(self.animation):
                self.frame = 0
            self.image = self.animation[int(self.frame)]
            self.rect = self.image.get_rect(center = self.rect.center)


    def update(self, player, enemy):  # updates every frame to maintain the player
        self.cooldown_handler()
        self.idle_listener()
        self.input_listener()
        self.animate()
        self.move()

