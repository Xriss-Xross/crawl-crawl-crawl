import pygame
from main import Game
from database import db_utils



class MenuUI:
    def __init__(self, levels):
        self.levels = levels

        #  displays the current time of that save slot
        self.time1 = db_utils().execute("SELECT Final_Time FROM Characters WHERE CharacterID = 1").fetchall()[0][0]
        self.time2 = db_utils().execute("SELECT Final_Time FROM Characters WHERE CharacterID = 2").fetchall()[0][0]
        self.time3 = db_utils().execute("SELECT Final_Time FROM Characters WHERE CharacterID = 3").fetchall()[0][0]
        self.time4 = db_utils().execute("SELECT Final_Time FROM Characters WHERE CharacterID = 4").fetchall()[0][0]
        
        #  makes the time human readable
        self.time1 = str(f"{str(int(self.time1 / 1000 // 60)).zfill(2)}:{str(int(self.time1 / 1000 % 60)).zfill(2)}")
        self.time2 = str(f"{str(int(self.time2 / 1000 // 60)).zfill(2)}:{str(int(self.time2 / 1000 % 60)).zfill(2)}")
        self.time3 = str(f"{str(int(self.time3 / 1000 // 60)).zfill(2)}:{str(int(self.time3 / 1000 % 60)).zfill(2)}")
        self.time4 = str(f"{str(int(self.time4 / 1000 // 60)).zfill(2)}:{str(int(self.time4 / 1000 % 60)).zfill(2)}")

        #  loads the surface to place things on and loads the font
        self.screen_surf = pygame.display.get_surface()
        self.x_font = pygame.font.Font('./assets/font/8_bit_font.ttf')

        #  these are all the attributes of UI elements to be placed which will be drawn in a seperate function
        self.x_board = pygame.Rect(673, 1, 45, 45)
        self.x_back_board = pygame.Rect(self.x_board.center[0]-25, self.x_board.center[1]-22, 48, 48)

        self.slot1_board = pygame.Rect(self.screen_surf.get_size()[0]/2-125, self.screen_surf.get_size()[1]/2-200, 250, 80)
        self.slot1_surf = self.x_font.render(f'Slot 1  {self.time1}', False, '#1B1233')
        self.slot1_rect = self.slot1_surf.get_rect(center = (self.slot1_board.center[0], self.slot1_board.center[1]))

        self.slot2_board = pygame.Rect(self.screen_surf.get_size()[0]/2-125, self.screen_surf.get_size()[1]/2-100, 250, 80)
        self.slot2_surf = self.x_font.render(f'Slot 2  {self.time2}', False, '#1B1233')
        self.slot2_rect = self.slot2_surf.get_rect(center = (self.slot2_board.center[0], self.slot2_board.center[1]))


        self.slot3_board = pygame.Rect(self.screen_surf.get_size()[0]/2-125, self.screen_surf.get_size()[1]/2, 250, 80)
        self.slot3_surf = self.x_font.render(f'Slot 3  {self.time3}', False, '#1B1233')
        self.slot3_rect = self.slot3_surf.get_rect(center = (self.slot3_board.center[0], self.slot3_board.center[1]))


        self.slot4_board = pygame.Rect(self.screen_surf.get_size()[0]/2-125, self.screen_surf.get_size()[1]/2+100, 250, 80)
        self.slot4_surf = self.x_font.render(f'Slot 4  {self.time4}', False, '#1B1233')
        self.slot4_rect = self.slot4_surf.get_rect(center = (self.slot4_board.center[0], self.slot4_board.center[1]))


    #  dedicated function to draw the quit button
    def draw_x(self, x, y):
        text_surf = self.x_font.render('X', False, '#DCF29D')
        self.x_rect = text_surf.get_rect(center = (x, y))
        self.screen_surf.blit(text_surf, self.x_rect)
 

    #  draws the UI elements
    def show(self):
        pygame.draw.rect(self.screen_surf, '#DCF29D', self.x_back_board)
        pygame.draw.rect(self.screen_surf, '#1B1233', self.x_board)

        pygame.draw.rect(self.screen_surf, '#DCF29D', self.slot1_board)
        pygame.draw.rect(self.screen_surf, '#DCF29D', self.slot2_board)
        pygame.draw.rect(self.screen_surf, '#DCF29D', self.slot3_board)
        pygame.draw.rect(self.screen_surf, '#DCF29D', self.slot4_board)

        self.screen_surf.blit(self.slot1_surf, self.slot1_rect)
        self.screen_surf.blit(self.slot2_surf, self.slot2_rect)
        self.screen_surf.blit(self.slot3_surf, self.slot3_rect)
        self.screen_surf.blit(self.slot4_surf, self.slot4_rect)

        self.draw_x(self.x_board.center[0]+2, self.x_board.center[1]+2)

        #  quits the game based on mouse position and if the mouse clicks
        if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pos()[0] in range(self.x_rect.left, self.x_rect.right) and pygame.mouse.get_pos()[1] in range(self.x_rect.top, self.x_rect.bottom):
            pygame.quit()

        #  launches the main game based on what save the user clicks on
        if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pos()[0] in range(self.slot1_rect.left, self.slot1_rect.right) and pygame.mouse.get_pos()[1] in range(self.slot1_rect.top, self.slot1_rect.bottom):
            pygame.quit()
            db_utils().execute(f"UPDATE Characters SET Max_Health = 4, Max_Shield = 10, Damage = 1, Speed = 3, XP = 0, Enemies_Defeated = 0, Enemies_Spawned = 0, Time = 0, Level = 0,  Map = '{self.levels}' WHERE CharacterID = 1")
            Game(1).play()
        if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pos()[0] in range(self.slot2_rect.left, self.slot2_rect.right) and pygame.mouse.get_pos()[1] in range(self.slot2_rect.top, self.slot2_rect.bottom):
            pygame.quit()
            db_utils().execute(f"UPDATE Characters SET Max_Health = 4, Max_Shield = 10, Damage = 1, Speed = 3, XP = 0, Enemies_Defeated = 0, Enemies_Spawned = 0, Time = 0, Level = 0,  Map = '{self.levels}' WHERE CharacterID = 2")
            Game(2).play()
        if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pos()[0] in range(self.slot3_rect.left, self.slot3_rect.right) and pygame.mouse.get_pos()[1] in range(self.slot3_rect.top, self.slot3_rect.bottom):
            pygame.quit()
            db_utils().execute(f"UPDATE Characters SET Max_Health = 4, Max_Shield = 10, Damage = 1, Speed = 3, XP = 0, Enemies_Defeated = 0, Enemies_Spawned = 0, Time = 0, Level = 0,  Map = '{self.levels}' WHERE CharacterID = 3")
            Game(3).play()
        if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pos()[0] in range(self.slot4_rect.left, self.slot4_rect.right) and pygame.mouse.get_pos()[1] in range(self.slot4_rect.top, self.slot4_rect.bottom):
            pygame.quit()
            db_utils().execute(f"UPDATE Characters SET Max_Health = 4, Max_Shield = 10, Damage = 1, Speed = 3, XP = 0, Enemies_Defeated = 0, Enemies_Spawned = 0, Time = 0, Level = 0,  Map = '{self.levels}' WHERE CharacterID = 4")
            Game(4).play()
