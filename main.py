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


def clamp_magnitude(vector: np.ndarray, max_length):
    sqrmag = vector_length(vector)
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
    def __init__(self) -> None:
        self.position = np.random.random(2) * 540 + 50
        self.velocity = (np.random.random(2)-0.5) * 300
        self.color = np.random.random(3) * 200 + 50
        self.radius = 10
        self.score = 0
        self.maxSpeed = np.random.random(2) * 300 + 300
        self.steer_strength = np.random.random() * 5 + 5
        self.angle = np.random.random()*360
        self.ill_radius = 20
        self.is_ill = bool(np.around(np.random.random()))

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
    def atan2(self):
        return np.arctan2(self.velocity[1], self.velocity[0])


class Obstruction:
    def __init__(self, x0, y0, x1, y1) -> None:
        self.start_pos = [x0, y0]
        self.end_pos = [x1, y1]


class DotController:
    def __init__(self, dot_amount: int, obs_list):
        self.dot_list: typing.List[Dot] = [Dot() for _ in range(dot_amount)]
        self.obs_list: typing.List[Obstruction] = obs_list
        self.accuracy = 20.0
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
        return np.random.random(2) * 540 + 50

    def is_ill(self):
        for dot in self.dot_list:
            for dot2 in self.dot_list:
                if not dot2 == dot:
                    d = vector_length(dot2.position-dot.position)
                    if d < dot.ill_radius+dot2.ill_radius:
                        if dot2.is_ill:
                            dot.is_ill = True

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

            for dot2 in self.dot_list:
                if not dot2 == dot:
                    dmd = dot2.position-dot.position
                    d = vector_length(dmd)
                    if d < dot.radius+dot2.radius:
                        n = dmd/d
                        # pv = (2*(dot.velocity[0]*n[0]+dot.velocity[1]*n[1] -
                        #         dot2.velocity[0]*n[0]-dot2.velocity[1]*n[1]))/(dot.steer_strength+dot.steer_strength)
                        # dot.velocity -= pv*n*dot.steer_strength
                        p = (dot.position+dot2.position)*0.5
                        dot.position = p-dot.radius*n

            dot.x += dot.velocity[0] * TICK
            dot.y += dot.velocity[1] * TICK

            if dot.x-dot.radius < 0:
                dot.x = dot.radius
                dot.velocity[0] *= -1

            if dot.y-dot.radius < 0:
                dot.y = dot.radius
                dot.velocity[1] *= -1

            if dot.x+dot.radius > WIDTH:
                dot.x = WIDTH-dot.radius
                dot.velocity[0] *= -1

            if dot.y+dot.radius > HEIGHT:
                dot.y = HEIGHT-dot.radius
                dot.velocity[1] *= -1
        self.is_ill()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


TARGET = False
obs = [Obstruction(240, 240, 400, 400)]
dot_controller = DotController(50, obs)

running = True


def redraw_window():
    # for o in obs:
    #    pygame.draw.lines(screen, RED, True, [o.start_pos, [
    #        o.start_pos[1], o.end_pos[0]], o.end_pos, [
    #        o.end_pos[1], o.start_pos[0]]])
    for dot in dot_controller:
        if TARGET:
            pygame.draw.circle(screen, GREEN, dot_controller.target,
                               dot_controller.accuracy, 1)

        if dot.is_ill:
            pass
            # pygame.draw.circle(screen, (200, 0, 0), dot.position, dot.radius)

        pygame.draw.circle(screen, dot.color, dot.position, dot.radius, 2)
        #  pygame.draw.circle(screen, (50, 50, 50),
        #                   dot.position, dot.ill_radius, 2)
        pygame.draw.line(screen, dot.color, dot.position,
                         (dot.x+np.cos(dot.atan2)*40,
                          dot.y+np.sin(dot.atan2)*40), 2)
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
