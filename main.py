import math

import numpy as np
import pygame

from Vector2 import Vector2

WIDTH, HEIGHT = 640, 640
FPS = 30
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
    def __init__(self, x, y, obs: list, target: list = None, other_dots: list = None) -> None:
        self.x: float = x
        self.y: float = y
        self.target = target
        if self.target is None:
            self.target = np.random.random(2) * 540 + 50
        self.maxSpeed = 10
        self.velocity = np.array([0, 0])
        self.obs_list: list = obs
        self.radius = 10
        self.other_dots = other_dots

    @property
    def pos(self):
        return [self.x, self.y]

    def update(self):
        steer_strength = 0.05

        distance = vector_length(
            np.array(self.target) - np.array(self.pos))

        if distance < 10:
            self.target = np.random.random(2) * 540 + 50

        desired_direction = normalize(
            np.array(self.target), np.array(self.pos))

        des_velocity = desired_direction * self.maxSpeed * -1
        des_steer = (des_velocity - self.velocity) * steer_strength
        acceleration = np.array(clamp_magnitude(des_steer, steer_strength))

        self.velocity = self.velocity + acceleration * clock.get_time()

        checked_pos = self.check_obstruction(
            self.velocity[0], self.velocity[1])

        self.x += checked_pos[0]
        self.y += checked_pos[1]

    def check_obstruction(self, x_pos, y_pos):
        return [x_pos, y_pos]


class Obstruction:
    def __init__(self, x0, y0, x1, y1) -> None:
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    @property
    def start_pos(self):
        return [self.x0, self.y0]

    @property
    def end_pos(self):
        return [self.x1, self.y1]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


def main():
    # obs = [Obstruction(160, 160, 240, 240), Obstruction(400, 160, 480, 480)]
    # dot_target = (np.random.random(2) * 640).tolist()

    # test_dot = [Dot(np.random.random() * 640, np.random.random() * 640, obs=obs) for _ in range(2)]
    # for d in test_dot:
    #     d.other_dots = test_dot

    running = True

    def redraw_window():
        # for o in obs:
        #    pygame.draw.lines(screen, GREEN, True, points=[
        #                      (o.x0, o.y0), (o.x1, o.y0), (o.x1, o.y1), (o.x0, o.y1)])
        # pygame.draw.circle(screen, RED, dot_target, 5)
        # pygame.draw.circle(screen, RED, dot_target, 100, 1)
        # for dot in test_dot:
        #     pygame.draw.circle(screen, GREEN, (dot.target[0], dot.target[1]), 5)
        #     pygame.draw.circle(screen, WHITE, (dot.x, dot.y), dot.radius, 2)
        #     pygame.draw.line(screen, WHITE, (dot.x, dot.y),
        #                    (dot.velocity[0] * 4 + dot.x,
        #                      dot.velocity[1] * 4 + dot.y), 1)
        pygame.draw.line(screen, WHITE, (Vector2.zero() +
                         320).position, (dir_to_mouse * 20 + 320).position)
        pygame.display.update()

    ticker = 1
    while running:
        clock.tick(FPS)
        # print(clock.get_time(), end='\r')
        ticker += 1

        mouse_pos = pygame.mouse.get_pos()
        dir_to_mouse = Vector2(mouse_pos[0], mouse_pos[1]).normalized

        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dot_target = pygame.mouse.get_pos()
                ticker = 1

        if ticker % 250 == 0:
            # dot_target = (np.random.random(2) * 320 + 320).tolist()
            ticker = 1

        # for dot in test_dot:
        #    dot.target = dot_target
        #    dot.update()

        print(ticker, end="\r")
        screen.fill(BLACK)

    pygame.quit()


if __name__ == "__main__":
    main()
