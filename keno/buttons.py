import pygame

from keno import WHITE, BLUE, RED, GREEN

class Button():
    def __init__(self,screen, x, y, w, h, msg, color=(BLUE), bcolor=(WHITE), tcolor=(WHITE)):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.msg = msg
        self.color = color
        self.bcolor = bcolor
        self.tcolor = tcolor
        self.enabled = True

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.w

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.h


    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def in_zone(self, coords):
        x, y = coords

        if x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h:
            return True
        return False

    def activated(self, coords):
        return self.in_zone(coords) and self.enabled

    def draw(self):
        tile_font = pygame.font.SysFont("comicsansms", round(self.h * .5))
        text = tile_font.render(self.msg, True, self.tcolor)
        textRect = text.get_rect()
        textRect.center = (self.x + self.w / 2, self.y + self.h / 2)
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))
        pygame.draw.rect(self.screen, self.bcolor, pygame.Rect(self.x, self.y, self.w, self.h), 2)


        self.screen.blit(text, textRect)

class Tile(Button):
    def __init__(self, screen, x, y, size, number):
        super().__init__(screen, x, y, size, size, str(number))
        self.number = number

    def draw(self):
        tile_font = pygame.font.SysFont("comicsansms", round(self.h * .5))
        text = tile_font.render(self.msg, True, self.tcolor)
        textRect = text.get_rect()
        textRect.center = (self.x + self.w / 2, self.y + self.h / 2)
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))
        pygame.draw.rect(self.screen, self.bcolor, pygame.Rect(self.x, self.y, self.w, self.h), 2)


        self.screen.blit(text, textRect)