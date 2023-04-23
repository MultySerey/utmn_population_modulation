import typing

import numpy as np
import pygame

# from Vector2 import Vector2

WIDTH, HEIGHT = 640, 640
FPS = 60
TICK = 1/FPS
DOT_RADIUS = 20
HALF_RADIUS = DOT_RADIUS / 2

PI = np.pi

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def vector_length(v: np.ndarray) -> float:
    return np.sqrt(v[0] ** 2 + v[1] ** 2)


def clamp_magnitude(vector, max_length):
    sqrmag: float = vector_length(np.array(vector))
    if sqrmag > max_length ** 2:
        mag: float = np.sqrt(sqrmag)
        normal_x = vector[0] / mag
        normal_y = vector[1] / mag
        return [normal_x * max_length, normal_y * max_length]
    return vector


def normalize(position: np.ndarray, target: np.ndarray):
    delta_pos = target - position
    distance = vector_length(delta_pos)
    return delta_pos / distance


def insideUnitCircle():
    a = np.random.random()
    b = np.sqrt(1-a**2)
    return np.array([a, b])


class Dot:
    def __init__(self) -> None:
        self.x: float = np.random.random() * 540 + 50
        self.y: float = np.random.random() * 540 + 50
        self.velocity = np.array([0, 0])
        self.maxSpeed = np.random.random() * 300 + 300
        self.steer_strength = np.random.random() * 5+5
        self.color = np.random.random(3) * 200 + 50
        self.radius = 10
        self.wander = 1

    @property
    def position(self):
        return [self.x, self.y]


class Obstruction:
    def __init__(self, x0, y0, x1, y1) -> None:
        self.start_pos = [x0, y0]
        self.end_pos = [x1, y1]


class DotController:
    def __init__(self, dot_amount: int, obs_list: typing.List[Obstruction]) -> None:
        self.dot_list: typing.List[Dot] = [Dot() for _ in range(dot_amount)]
        self.accuracy = 20.0
        self.obs_list = obs_list
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
        new = None
        check_list = []
        while True:
            new = np.random.random(2) * 540 + 50
            for obs in self.obs_list:
                if not (obs.start_pos[0] < new[0] < obs.end_pos[0] and obs.start_pos[1] < new[1] < obs.end_pos[1]):
                    check_list.append(True)
            if len(check_list) == len(self.obs_list):
                break
        return new

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
    obs = [Obstruction(240, 240, 400, 400)]
    dot_controller = DotController(50, obs)

    running = True

    def redraw_window():
        # for o in obs:
        #    pygame.draw.lines(screen, RED, True, [o.start_pos, [
        #        o.start_pos[1], o.end_pos[0]], o.end_pos, [
        #        o.end_pos[1], o.start_pos[0]]])
        for dot in dot_controller:
            pygame.draw.circle(screen, GREEN, dot_controller.target,
                               dot_controller.accuracy, 1)

            pygame.draw.circle(screen, dot.color, dot.position, 10, 1)
            atan = np.arctan2(
                dot_controller.target[1]-dot.y, dot_controller.target[0]-dot.x)
            pygame.draw.line(screen, dot.color, dot.position,
                             (dot.x+np.cos(atan)*40, dot.y+np.sin(atan)*40), 1)
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
