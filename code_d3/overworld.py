import pygame
from code_d3.data import levels


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if status == "a":
            self.image.fill("red")
        else:
            self.image.fill("gray")
        self.rect = self.image.get_rect(center=pos)

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2), self.rect.centery - (icon_speed/2), icon_speed, icon_speed)


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20, 20))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos


class Overworld():
    def __init__(self, start_level, max_level, surface, create_level):
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # logic
        self.move_dir = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.moving = False

        # setup screen
        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'a', self.speed)
            else:
                node_sprite = Node(node_data['node_pos'], 'l', self.speed)
            self.nodes.add(node_sprite)

    def draw_paths(self):
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]

        pygame.draw.lines(self.display_surface, 'red', False, points, 6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_d] and self.current_level < self.max_level:
                self.move_dir = self.get_movement_data(1)
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_a] and self.current_level > 0:
                self.move_dir = self.get_movement_data(-1)
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + target].rect.center)

        return (end - start).normalize()

    def update_icon_pos(self):
        if self.moving and self.move_dir:
            self.icon.sprite.pos += self.move_dir * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_dir = pygame.math.Vector2(0, 0)

    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)