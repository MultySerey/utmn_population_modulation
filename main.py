import math

import numpy as np
import pygame

import typing

# from Vector2 import Vector2

WIDTH, HEIGHT = 640, 640
FPS = 30
TICK = 1/FPS
DOT_RADIUS = 20
HALF_RADIUS = DOT_RADIUS / 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def vector_length(v: np.ndarray) -> float:
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


def clamp_magnitude(vector, max_length):
    sqrmag: float = vector_length(np.array(vector))
    if sqrmag > max_length ** 2:
        mag: float = math.sqrt(sqrmag)
        normal_x = vector[0] / mag
        normal_y = vector[1] / mag
        return [normal_x * max_length, normal_y * max_length]
    return vector


def normalize(position: np.ndarray, target: np.ndarray):
    delta_pos = target - position
    distance = vector_length(delta_pos)
    return delta_pos / distance


class Dot:
    def __init__(self, x, y, target: list = None) -> None:  # noqa
        self.x: float = x
        self.y: float = y
        self.target = target
        if self.target is None:
            self.target = np.random.random(2) * 540 + 50
        self.maxSpeed = 400.0
        self.velocity = np.array([0, 0])
        self.radius = 10
        self.accuracy = 10

    @property
    def pos(self):
        return [self.x, self.y]

    def update(self):
        steer_strength = 10.0

        distance = vector_length(
            np.array(self.target) - np.array(self.pos))

        if distance < self.accuracy:
            self.target = np.random.random(2) * 600 + 20

        desired_direction = normalize(
            np.array(self.target), np.array(self.pos))

        des_velocity = desired_direction * self.maxSpeed * -1
        des_steer = (des_velocity - self.velocity) * steer_strength
        acceleration = np.array(clamp_magnitude(des_steer, steer_strength))

        self.velocity = self.velocity + acceleration * TICK

        self.x += self.velocity[0] * TICK
        self.y += self.velocity[1] * TICK


class DotController:
    def __init__(self, dots: typing.List[Dot]) -> None:
        self.dots: typing.List[Dot] = dots


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


def main():
    test_dot = [Dot(np.random.random() * 640, np.random.random() * 640)
                for _ in range(1)]

    running = True

    def redraw_window():
        for dot in test_dot:
            pygame.draw.circle(screen, GREEN, dot.target, dot.accuracy, 1)
            pygame.draw.line(screen, GREEN, dot.pos, dot.target, 1)
            pygame.draw.circle(screen, WHITE, dot.pos, dot.radius, 1)
            pygame.draw.line(screen, WHITE, dot.pos,
                             (dot.velocity[0]/8 + dot.x,
                              dot.velocity[1]/8 + dot.y), 1)
            
        pygame.display.update()

    ticker = 1
    while running:
        clock.tick(FPS)
        ticker += 1

        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ticker = 1

        for dot in test_dot:
            dot.update()

        # print(prev_tick, ticker, end="    \r")
        screen.fill(BLACK)

    pygame.quit()


if __name__ == "__main__":
    main()
