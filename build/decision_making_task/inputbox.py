import pygame
import colors
from pygame.locals import *
import sys


class InputBox(pygame.sprite.Sprite):

    def __init__(self, screen, pos, size, q='', allowanswer=1, fontsize=24, textcolor=colors.black, a=''):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.boxcolor = colors.grey
        self.screen = screen
        self.textcolor = textcolor
        self.FONT = pygame.font.SysFont('Times New Roman', fontsize)
        self.a = a
        if q[-1] != ' ':
            q += ' '
        self.q = q
        self.allowanswer = allowanswer
        self.draw(self.screen)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_RETURN:
                return 1, self.a
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif self.allowanswer:
                if event.key == K_BACKSPACE:
                    self.a = self.a[:-1]
                else:
                    self.a += event.unicode
        return 0, None

    def blit_text(self, text, pos=(0, 0)):
        # put text in new line if too wide
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = self.FONT.size(' ')[0]  # The width of a space.
        max_width, max_height = self.image.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = self.FONT.render(word, 1, self.textcolor)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.image.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height + word_height//5 # Start on new row.
            if y > max_height:
                raise ValueError('text not fitting into the box!')

    def draw(self, screen):
        # Blit the text.
        self.image.fill(self.boxcolor)
        self.blit_text(self.q+self.a, pos=(0, 0))
        screen.blit(self.image, self.rect.topleft)
