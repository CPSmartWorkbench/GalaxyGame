import pygame

from gameLib import *

class World:
    def __init__(self, size, target_fps=70):
        self.ally_group = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.target_fps = target_fps
        self.size = size
        self.enemy_group = Formation(self, 3)
        self.score = 0
        self.player = None
        self.level = 0
        self.level_score_modifier = 1
    
    def draw(self, surface):
        self.ally_group.draw(surface)
        self.enemy_group.draw(surface)
    
    def update(self):
        self.ally_group.update()
        self.enemy_group.update()
        self.clock.tick(self.target_fps)
        self.delta_time = self.clock.get_time()
    
    def get_target_pos(self):
        return self.ally_group.sprites()[0].rect.center

