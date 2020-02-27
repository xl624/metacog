import pygame
import colors


class Button(pygame.sprite.Sprite):
    def __init__(self, fontsize, pos, unselected_col=colors.blue, selected_col=colors.lightOrange, text=''):
        """
        draw button and text in it, update on its color and status
        :param fontsize: fontsize of the text to draw (this determines button size too)
        :param pos: position of the button
        :param unselected_col: the color of the button when it is unselected
        :param selected_col: the color of the button when it is selected
        :param text: text to be displayed in the button
        """
        pygame.sprite.Sprite.__init__(self)
        self.textsurface = self.drawtext(text, fontsize)
        self.image = pygame.Surface((self.textsurface.get_rect().size[0] + 8, self.textsurface.get_rect().size[1] + 8))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.unselected_col = unselected_col
        self.select_col = selected_col
        self.selected = False
        self.fillColor = self.unselected_col

    def drawtext(self, text, fontsize):
        myFont = pygame.font.SysFont('Times New Roman', fontsize)
        textsurface = myFont.render(text, True, colors.black)
        return textsurface

    def update(self, screen, pos=None):
        status = None
        if pos:
            status = self.rect.collidepoint(pos)
            if status:
                self.selected = status - self.selected
            if self.selected:
                self.fillColor = colors.lightOrange
            else:
                self.fillColor = colors.blue
        self.image.fill(self.fillColor)
        self.image.blit(self.textsurface, (4, 4))
        screen.blit(self.image, self.rect.topleft)
        pygame.display.update()
        return status

    # def draw(self, screen):
    #     self.image.fill(self.fillColor)
    #     self.image.blit(self.textsurface, (4, 4))
    #     screen.blit(self.image, self.rect.topleft)
    #     pygame.display.update()
