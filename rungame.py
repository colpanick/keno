from os import chdir
from keno import game

import pygame


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("KENO!")

    chdir("keno")
    menu = game.Menu(screen)
    menu.run()