import typing

import numpy as np
import pygame

import setings

WIDTH = setings.WIDTH
HEIGHT = setings.HEIGHT
MIN_W_H = min(WIDTH, HEIGHT)
FPS = setings.FPS
TICK = 1/FPS

COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
}


class Dot:
    def __init__(self, id: int, pos: list = None) -> None:
        self.id = id
        if not pos:
            self.position = np.random.random(2)*0.8+0.1
        else:
            self.position = np.array(pos)
        self.radius = 0.0625

    @property
    def interval_x(self):
        return [self.x-self.radius, self.x+self.radius]

    @property
    def interval_y(self):
        return [self.y-self.radius, self.y+self.radius]

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

    def refresh(self):
        self.position = np.random.random(2)*0.8+0.1


class DotController:
    def __init__(self, dot_amount: int):
        self.dot_list: typing.List[Dot] = [Dot(i) for i in range(dot_amount)]
        self.dots_pos_x = {d.id: d.x for d in self.dot_list}
        self.overlaps()

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

    def overlaps(self):
        ids = np.array([dot.id for dot in self.dot_list])
        x_intervals = np.array([dot.interval_x for dot in self.dot_list])
        y_intervals = np.array([dot.interval_y for dot in self.dot_list])
        ind = np.argsort(x_intervals, axis=0)

        ids = np.squeeze(np.delete(ids[ind], 0, 1))
        x_intervals = np.squeeze(np.delete(x_intervals[ind], 0, 1))
        y_intervals = np.squeeze(np.delete(y_intervals[ind], 0, 1))

        overlap_list = set()

        for i in range(ids.size):
            for k in range(ids.size):
                if ids[i] != ids[k]:
                    if x_intervals[i][1] > x_intervals[k][0] and x_intervals[i][0] < x_intervals[k][1]:  # noqa
                        if y_intervals[i][1] > y_intervals[k][0] and y_intervals[i][0] < y_intervals[k][1]:  # noqa
                            overlap_list.add(ids[i])

        if len(overlap_list):
            return overlap_list
        else:
            return None


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)


running = True

dots = DotController(4)


def redraw_window():
    for d in dots:
        pygame.draw.circle(screen, COLORS["white"],
                           d.position*MIN_W_H,
                           d.radius*MIN_W_H, 1)
        text = font.render(str(d.id), False, COLORS["white"])
        textRect = text.get_rect()
        textRect.center = ((d.x*MIN_W_H, d.y*MIN_W_H))
        screen.blit(text, textRect)
    pygame.display.update()


while running:
    redraw_window()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                for d in dots:
                    d.refresh()
                print(dots.overlaps())

    screen.fill(COLORS["black"])

pygame.quit()
