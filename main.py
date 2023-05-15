import typing

import numpy as np
import pygame

# from Vector2 import Vector2

WIDTH, HEIGHT = 640, 640
FPS = 60
TICK = 1/FPS

PI = np.pi

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def sqr_mag(v: np.ndarray) -> float:
    return v[0] ** 2 + v[1] ** 2


def vector_length(v: np.ndarray) -> float:
    return np.sqrt(sqr_mag(v))


def clamp_magnitude(vector: np.ndarray, max_length):
    sqrmag = sqr_mag(vector)
    if sqrmag > (max_length ** 2):
        vector /= np.sqrt(sqrmag)
        return vector*max_length
    return vector


def normalize(delta_pos: np.ndarray):
    return delta_pos / vector_length(delta_pos)


def insideUnitCircle():
    a = np.random.random()
    b = np.sqrt(1-a**2)
    return np.array([a, b])


class Dot:
    def __init__(self, id) -> None:
        self.id = id
        self.position = np.random.random(2)
        self.velocity = (np.random.random(2)-0.5)*0.5
        self.color = WHITE
        self.radius = 0.02
        self.score = 0
        self.maxSpeed = np.random.random()
        self.steer_strength = np.random.random()+2
        self.angle = np.random.random()*360
        self.ill_radius = 0.04
        self._is_ill = np.around(np.random.random(), decimals=2)

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, value):
        self.position[0] = value

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, value):
        self.position[1] = value

    @property
    def is_ill(self):
        return self._is_ill

    @is_ill.setter
    def is_ill(self, value):
        self._is_ill = value
        if self._is_ill < 0:
            self.is_ill = 0
        if self._is_ill > 1:
            self.is_ill = 1

    @property
    def atan2(self):
        return np.arctan2(self.velocity[1], self.velocity[0])


class DotController:
    def __init__(self, dot_amount: int):
        self.dot_list: typing.List[Dot] = [Dot(i) for i in range(dot_amount)]
        self.accuracy = 0.025
        self.target = self.random_target()

    def __len__(self):
        return len(self.dot_list)

    def __getitem__(self, item):
        return self.dot_list[item]

    def __iter__(self):
        self.iter = 0
        return self

    def __next__(self):
        if self.iter < len(self.dot_list):
            out = self.dot_list[self.iter]
            self.iter += 1
            return out
        else:
            raise StopIteration

    def random_target(self):
        return np.random.random(2)

    def is_ill(self, dot: Dot, other: Dot):
        d = vector_length(other.position-dot.position)
        if d < dot.ill_radius+other.ill_radius:
            if other.is_ill:
                dot.is_ill += (dot.is_ill+other.is_ill)*0.01*np.random.random()

    def dot_by_dot_collision(self, dot: Dot, other: Dot):
        dmd = other.position-dot.position
        d = vector_length(dmd)
        if d < dot.radius+other.radius:
            n = dmd/d
            p = (dot.position+other.position)*0.5
            dot.position = p-dot.radius*n
            # другая коллизия
            pv = (2*(dot.velocity[0]*n[0]+dot.velocity[1]*n[1] -
                     other.velocity[0]*n[0]-other.velocity[1]*n[1]))/(dot.steer_strength+dot.steer_strength)
            dot.velocity -= pv*n*dot.steer_strength*0.5

    def wall_collision(self, dot: Dot):
        if dot.x-dot.radius < 0:
            dot.x = dot.radius
            dot.velocity[0] *= -1

        if dot.y-dot.radius < 0:
            dot.y = dot.radius
            dot.velocity[1] *= -1

        if dot.x+dot.radius > 1:
            dot.x = 1-dot.radius
            dot.velocity[0] *= -1

        if dot.y+dot.radius > 1:
            dot.y = 1-dot.radius
            dot.velocity[1] *= -1

    def update(self):
        for dot in self.dot_list:
            if TARGET:
                distance = vector_length(self.target - dot.position)

                if distance < self.accuracy:
                    self.target = self.random_target()
                    dot.score += 1

                desired_direction = normalize(self.target - dot.position)

                des_velocity = desired_direction * dot.maxSpeed
                des_steer = (des_velocity - dot.velocity) * dot.steer_strength
                acceleration = np.array(clamp_magnitude(
                    des_steer, dot.steer_strength))

                dot.velocity = dot.velocity + acceleration * TICK

            dot.is_ill -= 0.001

            for dot2 in self.dot_list:
                if not dot2 == dot:
                    self.dot_by_dot_collision(dot, dot2)
                    self.is_ill(dot, dot2)

            dot.x += dot.velocity[0] * TICK
            dot.y += dot.velocity[1] * TICK

            self.wall_collision(dot)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


TARGET = False
dot_controller = DotController(10)

running = True


def redraw_window():
    for dot in dot_controller:
        if TARGET:
            pygame.draw.circle(screen,
                               GREEN,
                               dot_controller.target*640,
                               dot_controller.accuracy*640,
                               1)

        if dot.is_ill:
            red_col = int(np.around(200*dot.is_ill))
            pygame.draw.circle(screen,
                               (red_col, 0, 0),
                               dot.position * 640,
                               dot.radius*640)

        pygame.draw.circle(screen,
                           dot.color,
                           dot.position * 640,
                           dot.radius * 640,
                           2)
        pygame.draw.circle(screen,
                           (50, 50, 50),
                           dot.position,
                           dot.ill_radius, 2)
        pygame.draw.line(screen,
                         dot.color,
                         dot.position*640,
                         ((dot.x+np.cos(dot.atan2)*0.1)*640,
                          (dot.y+np.sin(dot.atan2)*0.1)*640),
                         2)
    pygame.display.update()


ticker = 1
while running:
    clock.tick(FPS)
    ticker += 1

    redraw_window()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                TARGET = not TARGET

    dot_controller.update()

    screen.fill(BLACK)

pygame.quit()
