import numpy as np
import pygame

from jsoner import DotController

# from Vector2 import Vector2

WIDTH, HEIGHT = 640, 640
MIN_W_H = min(WIDTH, HEIGHT)
FPS = 60
TICK = 1/FPS

PI = np.pi

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


TARGET = False
dot_controller = DotController(10, 5)

running = True


def redraw_window():
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, MIN_W_H, MIN_W_H), 1)
    if TARGET:
        for t in dot_controller.target_list:
            pygame.draw.circle(screen, YELLOW, t.position*MIN_W_H,
                               dot_controller.accuracy*MIN_W_H, 1)
    for dot in dot_controller:
        if dot.is_ill:
            red_col = int(np.around(200*dot.is_ill))
            pygame.draw.circle(screen,
                               (red_col, 0, 0),
                               dot.position * MIN_W_H,
                               dot.radius*MIN_W_H)

        """pygame.draw.circle(screen,
                           (50, 50, 50),
                           dot.position*640,
                           dot.ill_radius*640, 2)"""
        pygame.draw.circle(screen,
                           dot.color,
                           dot.position * MIN_W_H,
                           dot.radius * MIN_W_H,
                           2)

        pygame.draw.line(screen,
                         dot.color,
                         dot.position*MIN_W_H,
                         dot.direction*MIN_W_H,
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
            if event.key == pygame.K_n:
                dot_controller.refresh_targets()

    dot_controller.update()

    screen.fill(BLACK)

pygame.quit()
