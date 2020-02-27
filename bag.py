import pygame
import colors


class Bag(pygame.sprite.Sprite):
    nPerRow = 4

    def __init__(self, w, v, screen, size, idx, total):
        """
        draw bags and update their select status and color
        :param w: weight
        :param v: value
        :param screen: screen to draw on
        :param size: size of the bag
        :param idx: idx of the bag in bagList (starting from 1)
        :param total: how many bags in total
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.weight = w
        self.value = v
        self.win = screen
        self.size = size
        self.fillColor = colors.blue
        self.selected = 0
        self.idx = idx
        self.total = total
        self.rect = self.image.get_rect()
        self.rect.topleft = self.getPos()

    def getPos(self):
        winSize = self.win.get_size()
        sidePad = winSize[0] // 9
        topPad = winSize[1] // 10
        nrow = (self.total - 1) // Bag.nPerRow + 1
        idxRow = (self.idx - 1) // Bag.nPerRow + 1
        if idxRow < nrow:
            ncol = 4
            idxCol = (self.idx - 1) % Bag.nPerRow + 1
        else:
            ncol = (self.total - 1) % Bag.nPerRow + 1
            idxCol = self.idx - (nrow - 1) * Bag.nPerRow
        width = (winSize[0] - sidePad * 2) // ncol
        height = (winSize[1] - topPad) // nrow
        topx = (idxCol - 1) * width + sidePad
        topy = (idxRow - 1) * height + topPad
        pos = (width - self.size[0]) // 2 + topx, (height - self.size[1]) // 3 * 2 + topy
        return pos

    def text(self):
        myFont = pygame.font.SysFont('Times New Roman', self.size[0] // 4, bold=True)
        vSurface = myFont.render('$' + str(self.value), True, colors.black)
        wSurface = myFont.render(str(self.weight) + 'kg', True, colors.black)
        return vSurface, wSurface

    def update(self, pos=None, forceSelect=False,forceUnselect=False):
        clicked = 0
        if pos:
            clicked = self.rect.collidepoint(pos)
            if clicked:
                self.selected = clicked - self.selected
                if self.selected:
                    self.fillColor = colors.lightOrange
                else:
                    self.fillColor = colors.blue
        if forceSelect:
            self.selected = True
            self.fillColor = colors.lightOrange
        if forceUnselect:
            self.selected = False
            self.fillColor = colors.blue
        self.image.fill(self.fillColor)
        vSurface, wSurface = self.text()
        vSize = vSurface.get_size()
        wSize = wSurface.get_size()
        self.image.blit(vSurface, ((self.size[0] - vSize[0]) // 2, (self.size[1] / 2 - vSize[1]) // 2))
        self.image.blit(wSurface,
                        ((self.size[0] - wSize[0]) // 2, (self.size[1] / 2 - wSize[1]) // 2 + self.size[1] / 2))
        return clicked, self.selected


