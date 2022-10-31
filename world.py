import pygame

class World:
    def __init__(self, target_fps=70):
        self.ally_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.target_fps = target_fps
    
    def draw(self, surface):
        self.ally_group.draw(surface)
        self.enemy_group.draw(surface)
    
    def update(self):
        self.ally_group.update()
        self.enemy_group.update()
        self.clock.tick(self.target_fps)
        self.delta_time = self.clock.get_time()
