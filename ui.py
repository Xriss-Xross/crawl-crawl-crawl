import pygame


class UI:
    def __init__(self):
        self.screen_surf = pygame.display.get_surface()
        self.font = pygame.font.Font('./assets/font/8_bit_font.ttf')

        self.stats_board = pygame.Rect(1, 1, 239, 45)

    def draw_stat(self, x, y, info, id):
        text_surf = self.font.render(id+str(info), False, '#DCF29D')
        text_rect = text_surf.get_rect(midleft = (x, y))

        self.screen_surf.blit(text_surf, text_rect)

    def draw_time(self, x, y, info, id):
        text_surf = self.font.render(f'{id} {str(int(info / 1000 // 60))}:{str(int(info / 1000 % 60))}', False, '#DCF29D')
        text_rect = text_surf.get_rect(midleft = (x, y))

        self.screen_surf.blit(text_surf, text_rect)

    def show(self, health, shield, time):
        pygame.draw.rect(self.screen_surf, '#1B1233', self.stats_board)
        self.draw_stat(14, 22.5, health, 'H:')
        self.draw_stat(90, 22.5, shield, 'S:')
        self.draw_time(160, 22.5, time, 'T:')