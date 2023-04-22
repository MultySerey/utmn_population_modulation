import math
import typing

import numpy as np
import pygame

# from Vector2 import Vector2

WIDTH, HEIGHT = 640, 640
FPS = 60
TICK = 1/FPS
DOT_RADIUS = 20
HALF_RADIUS = DOT_RADIUS / 2

PI = math.pi

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
    def __init__(self) -> None:
        self.x: float = np.random.random() * 540 + 50
        self.y: float = np.random.random() * 540 + 50
        self.velocity = np.array([0, 0])
        self.maxSpeed = np.random.random() * 300 + 300
        self.steer_strength = np.random.random() + 10
        self.color = WHITE
        self.radius = 10

    @property
    def position(self):
        return [self.x, self.y]


class DotController:
    def __init__(self, dot_amount: int) -> None:
        self.dot_list: typing.List[Dot] = [Dot() for _ in range(dot_amount)]
        self.target = self.random_target()
        self.accuracy = 20.0

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
        return np.random.random(2) * 540 + 50

    def update(self):
        for dot in self.dot_list:
            distance = vector_length(
                np.array(self.target) - np.array(dot.position))

            if distance < self.accuracy:
                self.target = self.random_target()

            desired_direction = normalize(
                np.array(self.target), np.array(dot.position))

            des_velocity = desired_direction * dot.maxSpeed * -1
            des_steer = (des_velocity - dot.velocity) * dot.steer_strength
            acceleration = np.array(clamp_magnitude(
                des_steer, dot.steer_strength))

            dot.velocity = dot.velocity + acceleration * TICK

            dot.x += dot.velocity[0] * TICK
            dot.y += dot.velocity[1] * TICK


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


def main():
    dot_controller = DotController(1)

    running = True

    def redraw_window():
        for dot in dot_controller:
            pygame.draw.circle(screen, GREEN, dot_controller.target,
                               dot_controller.accuracy, 1)
            # pygame.draw.line(screen, GREEN, dot.position,
            #                   dot_controller.target, 1)
            pygame.draw.circle(screen, dot.color, dot.position, 10, 1)
            atan = math.atan2(
                dot_controller.target[1]-dot.y, dot_controller.target[0]-dot.x)
            pygame.draw.line(screen, dot.color, dot.position,
                             (dot.x+math.cos(atan)*40, dot.y+math.sin(atan)*40), 1)
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

        dot_controller.update()

        screen.fill(BLACK)

    pygame.quit()


if __name__ == "__main__":
    main()
