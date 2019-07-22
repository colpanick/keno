import pygame

RESOLUTION = (1024, 768)
CAPTION = "KENO!"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 30, 150)
GREEN = (0, 200, 0)
RED = (175, 30, 30)

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()