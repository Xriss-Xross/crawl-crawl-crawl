import pygame


class UI:
    def __init__(self):
        self.screen_surf = pygame.display.get_surface()
        self.font = pygame.font.Font('./assets/font/8_bit_font.ttf')

        self.x_font = pygame.font.Font('./assets/font/8_bit_font.ttf', 25)

        self.stats_board = pygame.Rect(1, 1, 239, 45)
        self.x_board = pygame.Rect(673, 1, 45, 45)

    def draw_stat(self, x, y, info, id):
        text_surf = self.font.render(id+str(info), False, '#DCF29D')
        text_rect = text_surf.get_rect(midleft = (x, y))

        self.screen_surf.blit(text_surf, text_rect)

    def draw_time(self, x, y, info, id):
        text_surf = self.font.render(f'{id} {str(int(info / 1000 // 60))}:{str(int(info / 1000 % 60))}', False, '#DCF29D')
        text_rect = text_surf.get_rect(midleft = (x, y))

        self.screen_surf.blit(text_surf, text_rect)

    def draw_x(self, x, y):
        text_surf = self.x_font.render('X', False, '#DCF29D')
        self.x_rect = text_surf.get_rect(center = (x, y))
        self.screen_surf.blit(text_surf, self.x_rect)


    def show(self, health, shield, time):

        pygame.draw.rect(self.screen_surf, '#1B1233', self.stats_board)
        pygame.draw.rect(self.screen_surf, '#1B1233', self.x_board)
        self.draw_stat(14, 22.5, health, 'H:')
        self.draw_stat(90, 22.5, shield, 'S:')
        self.draw_time(160, 22.5, time, 'T:')
        self.draw_x(self.x_board.center[0]+2, self.x_board.center[1]+2)

        if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pos()[0] in range(self.x_rect.left, self.x_rect.right) and pygame.mouse.get_pos()[1] in range(self.x_rect.top, self.x_rect.bottom):
            pygame.quit()
