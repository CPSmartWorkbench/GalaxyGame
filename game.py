import pygame
from enum import Enum
import sys
import math

from gameLib import *
from track import HandInput

BACKGROUND_COLOR = (0, 0, 0)
HIGHSCORE_PATH = 'hs.txt'
TIMEOUT = 1000 * 5 * 60 # 5 minutes

DEFAULT_SCREEN_SIZE = (800, 600)

LIFE_IMAGE = pygame.image.load('textures/HeartPoint.png')

class GameState(Enum):
    IN_MENU = 0
    PLAYING_GAME = 1
    QUIT = 2

class Game:

    def __init__(self, display, camera_input=True, fullscreen=False):
        pygame.init()

        if (display > pygame.display.get_num_displays() - 1):
            display = pygame.display.get_num_displays() - 1

        if (fullscreen):
            screen_size = pygame.display.get_desktop_sizes()[display]
        else:
            screen_size = DEFAULT_SCREEN_SIZE

        self.screen = pygame.display.set_mode(screen_size, display=display)

        if (fullscreen):
            pygame.display.toggle_fullscreen()

        self.state = GameState.IN_MENU

        self.input = None
        if (camera_input):
            self.input = HandInput()

        self.font = pygame.font.Font('8bitOperatorPlus-Regular.ttf', 30)

        self.world = None
        self.player = None

        self.heart_image = pygame.transform.scale(LIFE_IMAGE, (DEFAULT_SIZE, DEFAULT_SIZE))
        self.heart_image.set_colorkey((0, 0, 0))

        with open(HIGHSCORE_PATH, 'r') as f:
            self._highscore = int(f.read())

        self.menu = Menu(screen_size, self.font, self._highscore)

        self.background = Background(screen_size)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.background.draw(self.screen)

        if self.state == GameState.PLAYING_GAME:
            self.world.draw(self.screen)

            img = self.font.render(f"Score: {self.world.score}", True, (255, 255, 255))

            self.screen.blit(img, (0, 0))

            img = self.font.render(f"Level: {self.world.level}", True, (255, 255, 255))

            self.screen.blit(img, (0, img.get_height()))

            health = math.ceil(self.player.health / PLAYER_STARTING_HEALTH * 3)

            for heart in range(1, health + 1):
                self.screen.blit(self.heart_image, (self.screen.get_width() - self.heart_image.get_width() * heart, 0))

        if self.state == GameState.IN_MENU:
            self.menu.group.draw(self.screen)

            if self.input is not None:
                user_input = self.input.process_position_input()                
                over_start_button = 0

                for pos in user_input:
                    pos = (pos[0] * self.screen.get_width(), pos[1] * self.screen.get_height())
                    pygame.draw.circle(self.screen, (255, 100, 0), pos, 6)

                    if (self.menu.is_over_start_button(*pos)):
                        over_start_button += 1
                
                if over_start_button == 2:
                    self.start_game()

        pygame.display.flip()

    def handle_keypress(self, key, press_type):
        if (key == pygame.K_ESCAPE and press_type == pygame.KEYDOWN):
            self.state = GameState.QUIT

        if (self.state == GameState.IN_MENU):
            if (key == pygame.K_RETURN and press_type == pygame.KEYDOWN):
                self.start_game()

        if (self.state == GameState.PLAYING_GAME):
            if (key == pygame.K_SPACE and press_type == pygame.KEYDOWN):
                self.player.fire()
            elif (key == pygame.K_UP and press_type == pygame.KEYDOWN):
                self.world.level += 1
            elif (key == pygame.K_DOWN and press_type == pygame.KEYDOWN):
                self.world.level -= 1
    
    def run(self):
        while self.state != GameState.QUIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameState.QUIT
                
                elif event.type == EVENT_GAMEOVER:
                    self._highscore = max(self._highscore, self.world.score)
                    self.menu.update_highscore(self._highscore)
                    self.state = GameState.IN_MENU

                elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                    self.handle_keypress(event.key, event.type)

            if self.state == GameState.PLAYING_GAME:
                process = self.poll_process()

                if process is not None:
                    self.timeout_timer = pygame.time.get_ticks() + TIMEOUT
                    fire, move = process

                    self.player.position = self.player.position.lerp(Vector((1 - move) * self.world.size[0], self.player.position.y), 0.6)
                    if (fire):
                        self.player.fire()
                
                elif pygame.time.get_ticks() > self.timeout_timer and self.input is not None:
                    print(f'User timeout after {TIMEOUT} ms')
                    self.player.kill()

                self.world.update()
            self.draw()

        with open(HIGHSCORE_PATH, 'w') as f:
            f.write(str(self._highscore))

    def start_game(self):
        self.timeout_timer = pygame.time.get_ticks() + TIMEOUT
        self.world = World(self.screen.get_size())
        self.player = Player(self.world, self.screen.get_size())
        self.world.ally_group.add(self.player)
        self.state = GameState.PLAYING_GAME

    def poll_process(self):
        process = None
        if self.input is not None:
            process = self.input.process_game_input()
        
        return process

def main():
    debug_mode = (len(sys.argv) > 1 and sys.argv[1] == 'debug')

    game = Game([1, 0][debug_mode], camera_input=(not debug_mode), fullscreen=(not debug_mode))
    game.run()

if __name__ == "__main__":
    main()