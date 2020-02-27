import pygame
import colors


class DragScale(pygame.sprite.Sprite):
    def __init__(self, screen, min=1, max=10, discrete=True, screenWidth=1200, pos=(100, 100), color=colors.black):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((screenWidth - 2 * pos[0], 10))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.min = min
        self.max = max
        self.dragging = False
        self.screen = screen
        self.fillColor = color

    def draw(self, screen):
        # Blit the text.
        self.image.fill(self.fillColor)
        self.image.blit(self.q_surface, (0, 0))
        self.image.blit(self.a_surface, (self.FONT.size(self.q)[0], 0))
        screen.blit(self.image, self.rect.topleft)


rectangle = pygame.rect.Rect(176, 134, 17, 17)
rectangle_draging = False

# - mainloop -

clock = pygame.time.Clock()

running = True

while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y

    # - updates (without draws) -

    # empty

    # - draws (without updates) -

    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, rectangle)

    pygame.display.flip()

    # - constant game speed / FPS -

    clock.tick(FPS)

# - end -

pygame.quit()
