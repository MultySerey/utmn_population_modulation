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
                           d.position*800,
                           d.radius*800, 1)
        text = font.render(str(d.id), False, COLORS["white"])
        textRect = text.get_rect()
        textRect.center = ((d.x*800, d.y*800))
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
                print(dots.dots_pos_x)

    screen.fill(COLORS["black"])

pygame.quit()
