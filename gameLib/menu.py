import pygame

TITLE_TEXTURE = pygame.image.load('textures/Handaga.png')

class Menu:
    def __init__(self, screen_size, font, highscore):
        self.group = pygame.sprite.Group()
        self.font = font
        self.screen_size = screen_size
        
        title = pygame.sprite.Sprite(self.group)
        title.image = TITLE_TEXTURE
        title.rect = title.image.get_rect()

        screen_x, screen_y = screen_size

        title.rect.x = screen_x / 2 - title.rect.width / 2
        title.rect.y = screen_y / 2 - title.rect.height - 100

        img = font.render("Hold firing hand above moving hand, pinch to fire", False, (255, 255, 255))
        info = pygame.sprite.Sprite(self.group)
        info.image = img
        info.rect = img.get_rect()
        info.rect.x = screen_x / 2 - info.rect.width / 2
        info.rect.y = screen_y - info.rect.height - 20

        img = font.render("Hold up hands", False, (255, 255, 255))
        info2 = pygame.sprite.Sprite(self.group)
        info2.image = img
        info2.rect = img.get_rect()
        info2.rect.x = screen_x / 2 - info2.rect.width / 2
        info2.rect.y = screen_y - info2.rect.height - 60

        img = font.render(f"High Score: {highscore}", False, (255, 255, 255))
        self.highscore_text = pygame.sprite.Sprite(self.group)
        self.highscore_text.image = img
        self.highscore_text.rect = img.get_rect()
        self.highscore_text.rect.x = screen_x / 2 - self.highscore_text.rect.width / 2
        self.highscore_text.rect.y = screen_y / 2 - self.highscore_text.rect.height / 2 + 100

        img = pygame.Surface((300, 70))
        img.fill((50, 50, 50))
        self.start_button = pygame.sprite.Sprite(self.group)
        self.start_button.image = img
        self.start_button.rect = img.get_rect()
        self.start_button.rect.x = screen_x / 2 - self.start_button.rect.width / 2
        self.start_button.rect.y = screen_y / 2 - self.start_button.rect.height / 2

        img = font.render(f"Start Game", False, (255, 255, 255))
        sg = pygame.sprite.Sprite(self.group)
        sg.image = img
        sg.rect = img.get_rect()
        sg.rect.x = screen_x / 2 - sg.rect.width / 2
        sg.rect.y = screen_y / 2 - sg.rect.height / 2
    
    def is_over_start_button(self, x, y):
        return self.start_button.rect.x <= x and x <= self.start_button.rect.x + self.start_button.rect.width and \
            self.start_button.rect.y <= y and y <= self.start_button.rect.y + self.start_button.rect.height
    
    def update_highscore(self, highscore):
        screen_x, screen_y = self.screen_size
        img = self.font.render(f"High Score: {highscore}", False, (255, 255, 255))
        self.highscore_text.image = img
        self.highscore_text.rect = img.get_rect()
        self.highscore_text.rect.x = screen_x / 2 - self.highscore_text.rect.width / 2
        self.highscore_text.rect.y = screen_y / 2 - self.highscore_text.rect.height / 2 + 100