import pygame
import sys

from code_d2.settings import *
from code_d2.level import Level
from code_d2.game_data import level_0

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("gray")
    level.run()

    pygame.display.update()
    clock.tick(60)