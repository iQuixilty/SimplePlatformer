import pygame
import sys

from code_d2.settings import *
from code_d2.level import Level
from code_d2.game_data import level_0
from code_d2.overworld import Overworld


class Game:
    def __init__(self):
        self.max_level = 0
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'o'

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = 'l'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'o'

    def run(self):
        if self.status == 'o':
            self.overworld.run()
        else:
            self.level.run()


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("gray")
    game.run()

    pygame.display.update()
    clock.tick(60)
