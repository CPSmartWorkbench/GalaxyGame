import pygame
import random
import math

from gameLib import *

MOVE_SPEED = 0.07
MOVE_PADDING = 20

ADVANCE_MIN = 3000
ADVANCE_MAX = 4500

ATTACK_Y_MIN = 200
ATTACK_Y_MAX = 300

FIRE_TIME = 2400

TWO_PI = 6.28318530718
FIRE_ANGLE = 1.57079632679
ROTARY_FIRE_TIMER = 800

class Formation(pygame.sprite.Group):

    def __init__(self, world, size, spacing=5):
        super().__init__()

        self._size = 2 * size - 1
        self._spacing = spacing + DEFAULT_SIZE
        self._world = world

        self._main_ships = []
        self._attack_ships = []
        self._target_pos_dict = {}

        self._center_x = world.size[0] / 2
        self._center_y = world.size[1] / 4

        self._width = self._size * self._spacing - spacing
        self._height = self._size * self._spacing - spacing

        self._move_x = MOVE_SPEED

        self._min_x = self._width / 2 + MOVE_PADDING
        self._max_x = world.size[0] - self._width / 2 - MOVE_PADDING

        self._level_generator_instance = None

    def _square_level_generator(self):
        self._main_ships = []
        self._attack_ships = []
        self._target_pos_dict = {}

        self._center_x = self._world.size[0] / 2
        self._center_y = self._world.size[1] / 4

        advance_timer = pygame.time.get_ticks() + random.randint(1000, 2000)
        enemies_left = True
        fire_timer = pygame.time.get_ticks() + FIRE_TIME

        # Generate enemies in a square
        for i in range(self._size):
            for j in range(self._size):
                x = self._center_x + self._spacing * (j - self._size // 2)
                y = self._center_y + self._spacing * (i - self._size // 2)

                enemy = Enemy(self._world, Vector(x, y))

                self._main_ships.append(enemy)
                self.add(enemy)

        # Update generator loop
        while enemies_left:
            self._center_x += self._move_x * self._world.delta_time
            if (self._move_x > 0 and self._center_x > self._max_x - random.randint(0, 100)):
                self._move_x = -MOVE_SPEED * self._level_to_speed_modifer(self._world.level)

            elif (self._move_x < 0 and self._center_x < self._min_x + random.randint(0, 100)):
                self._move_x = MOVE_SPEED * self._level_to_speed_modifer(self._world.level)
    
            if (advance_timer < pygame.time.get_ticks() and len(self._attack_ships) < 4):
                advance_timer = pygame.time.get_ticks() + random.randint(ADVANCE_MIN, ADVANCE_MAX)
                if (len(self._main_ships) > 0):
                    ship = random.choice(self._main_ships)

                    self._main_ships.remove(ship)
                    self._attack_ships.append(ship)

                    target = Vector(
                        self._world.player.position.x,
                        random.randint(self._world.size[1] - ATTACK_Y_MAX, self._world.size[1] - ATTACK_Y_MIN)
                    )

                    self._target_pos_dict[ship] = (Vector(ship.position.x, ship.position.y), target)

            enemies_left = False
            temp_array = []
            for i in range(len(self._main_ships)):
                ship = self._main_ships[i]
                ship.position.x = ship.position.x + self._move_x * self._world.delta_time

                if ship.alive():
                    enemies_left = True
                    temp_array.append(ship)

            self._main_ships = temp_array

            fire = pygame.time.get_ticks() > fire_timer

            temp_array = []
            for i in range(len(self._attack_ships)):
                ship = self._attack_ships[i]
                distance_to_target = self._target_pos_dict[ship][1].distance(ship.position)

                if (fire and distance_to_target < 20):
                    ship.fire()

                elif (distance_to_target >= 1000):
                    ship.kill()

                elif (distance_to_target >= 20):
                    d = self._target_pos_dict[ship][1] - self._target_pos_dict[ship][0]
                    d = d * 0.001 * self._world.delta_time * self._level_to_speed_modifer(self._world.level)
                    ship.position.x = ship.position.x + d.x
                    ship.position.y = ship.position.y + d.y

                if ship.alive():
                    enemies_left = True
                    temp_array.append(ship)

            if fire:
                fire_timer = pygame.time.get_ticks() + FIRE_TIME + random.randint(-50, 50)
            
            self._attack_ships = temp_array

            yield True
        
        yield False

    def _circle_level_generator(self):
        self._main_ships = []

        self._center_x = self._world.size[0] / 2
        self._center_y = self._world.size[1] / 4

        advance_timer = pygame.time.get_ticks() + random.randint(1000, 2000)
        enemies_left = True
        fire_timer = pygame.time.get_ticks() + FIRE_TIME

        # Generate enemies in a circle
        n = (self._size ** 2) // 2
        radius = self._spacing * 2
        rotary_ships = []
        for i in range(n):
            x = self._center_x + radius * math.cos(i / n * TWO_PI)
            y = self._center_y + radius * math.sin(i / n * TWO_PI)

            enemy = Enemy(self._world, Vector(x, y))

            self._main_ships.append(enemy)
            rotary_ships.append(enemy)
            self.add(enemy)

        rotation_offset = 0
        fire_timer = pygame.time.get_ticks() + ROTARY_FIRE_TIMER

        # Update generator loop
        while enemies_left:
            self._center_x += self._move_x * self._world.delta_time
            if (self._move_x > 0 and self._center_x > self._max_x - random.randint(0, 100)):
                self._move_x = -MOVE_SPEED

            elif (self._move_x < 0 and self._center_x < self._min_x + random.randint(0, 100)):
                self._move_x = MOVE_SPEED

            rotation_offset += 0.0005 * self._world.delta_time * self._level_to_speed_modifer(self._world.level)

            enemies_left = False
            temp_array = []

            for i in range(len(rotary_ships)):
                ship = rotary_ships[i]
                radians = (i / n * TWO_PI + rotation_offset) % TWO_PI
                ship.position.x = self._center_x + radius * math.cos(radians)
                ship.position.y = self._center_y + radius * math.sin(radians)

                if (radians < FIRE_ANGLE + 0.1 and radians > FIRE_ANGLE - 0.1):
                    if (pygame.time.get_ticks() > fire_timer):
                        ship.fire()
                        fire_timer = pygame.time.get_ticks() + ROTARY_FIRE_TIMER
                
                
                if ship.alive():
                    enemies_left = True
                    temp_array.append(ship)

            self._main_ships = temp_array

            yield True
        
        yield False

    def update(self):
        if self._level_generator_instance is None:
            self._world.level += 1
            if (random.random() < 0.7):
                self._world.level_score_modifier = int(5 * self._level_to_speed_modifer(self._world.level))
                self._level_generator_instance = self._square_level_generator()
            else:
                self._world.level_score_modifier = int(15 * self._level_to_speed_modifer(self._world.level))
                self._level_generator_instance = self._circle_level_generator()
        
        else:
            if not next(self._level_generator_instance):
                self._level_generator_instance = None

        pygame.sprite.Group.update(self)
    
    def _level_to_speed_modifer(self, level):
        return math.log(level / 2 + 1) + 1
    
