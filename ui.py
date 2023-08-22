import pygame


class UI:
    def __init__(self):
        self.screen_surf = pygame.display.get_surface()
        self.font = pygame.font.Font('./assets/font/8_bit_font.ttf')

        self.stats_board = pygame.Rect(1, 1, 239, 45)

    def draw_stat(self, x, y, info, id):
        text_surf = self.font.render(id+str(int(info)), False, '#DCF29D')
        text_rect = text_surf.get_rect(midleft = (x, y))

        self.screen_surf.blit(text_surf, text_rect)

    def show(self, health, shield, xp):
        pygame.draw.rect(self.screen_surf, '#1B1233', self.stats_board)
        self.draw_stat(4, 22.5, health, 'H:')
        self.draw_stat(80, 22.5, shield, 'S:')
        self.draw_stat(150, 22.5, xp, 'XP:')
