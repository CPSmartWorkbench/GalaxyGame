import pygame

from gameLib import *

ENEMY_STARTING_HEALTH = 10

ENEMY_TEXTURE = pygame.image.load('textures/alien_blue.png')

class Enemy(Entity):

    def __init__(self, world, position : Vector):
        super().__init__(world, position, ENEMY_STARTING_HEALTH, ENEMY_TEXTURE)

    def fire(self):
        if self.alive():
            missile = EnemyMissile(self.world, self.position)
            self.world.enemy_group.add(missile)

    def update(self):
        super().update()
    
    def kill(self):
        self.world.score += self.world.level_score_modifier
        super().kill()