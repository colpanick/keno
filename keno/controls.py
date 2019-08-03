import pygame

from keno import WHITE, BLUE

class Control():
    def __init__(self, screen, x, y, w, h):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
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


class Button(Control):

    def __init__(self,screen, x, y, w, h, msg, color=(BLUE), bcolor=(WHITE), tcolor=(WHITE), image=None):
        super().__init__(screen, x, y, w, h)
        self.msg = msg
        self.color = color
        self.bcolor = bcolor
        self.tcolor = tcolor
        self.__image = image
        if self.__image:
            self.w, self.h = self.__image.get_rect()[2:]

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image
        self.w, self.h = self.__image.get_rect()[2:]

    def draw(self):
        tile_font = pygame.font.SysFont("comicsansms", round(self.h * .5))
        text = tile_font.render(self.msg, True, self.tcolor)
        textRect = text.get_rect()
        textRect.center = (self.x + self.w / 2, self.y + self.h / 2)

        if self.__image:
            self.screen.blit(self.__image, (self.x, self.y))
        else:
            pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))
            pygame.draw.rect(self.screen, self.bcolor, pygame.Rect(self.x, self.y, self.w, self.h), 2)


        self.screen.blit(text, textRect)

class Tile(Button):
    def __init__(self, screen, x, y, size, number, image=None):
        super().__init__(screen, x, y, size, size, str(number), image)
        self.number = number




class Text(Control):

    def __init__(self, screen, x, y, msg, font_name="comicsansms", color=WHITE, size=22):
        self.__msg = msg
        self.font_name = font_name
        self.color = color
        self.size = size
        self.font = pygame.font.SysFont(self.font_name, self.size)
        self.text = self.font.render(self.msg, True, self.color)
        self.w, self.h = self.text.get_rect()[2:]

        super().__init__(screen, x, y, self.w, self.h)

    @property
    def msg(self):
        return self.__msg

    @msg.setter
    def msg(self, msg):
        self.__msg = msg
        self.text = self.font.render(self.__msg, True, self.color)
        self.w, self.h = self.text.get_rect()[2:]


    def draw(self):
        self.screen.blit(self.text, (self.x,self.y,self.w,self.h))


class Image(Control):
    def __init__(self, screen, x, y, filename):
        self.filename = filename
        self.image = pygame.image.load(filename)
        self.w, self.h = self.image.get_rect()[2:]

        super().__init__(screen, x, y, self.w, self.h)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))