import numpy as np
import pygame

from jsoner import DotController

# from Vector2 import Vector2

WIDTH, HEIGHT = 640, 640
MIN_W_H = min(WIDTH, HEIGHT)
FPS = 60
TICK = 1/FPS

COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blu": (0, 0, 255),
    "yellow": (255, 255, 0),
}


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


TARGET = False
dot_controller = DotController(10, 5, TICK)

running = True


def redraw_window():
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, MIN_W_H, MIN_W_H), 1)

    for dot in dot_controller:
        if dot_controller.mode != 0:
            pygame.draw.circle(screen, COLORS["green"],
                               dot.target.position*MIN_W_H,
                               dot_controller.accuracy*MIN_W_H, 1)
        if dot.is_ill:
            red_col = int(np.around(200*dot.is_ill))
            pygame.draw.circle(screen, (red_col, 0, 0),
                               dot.position * MIN_W_H,
                               dot.radius*MIN_W_H)

        """pygame.draw.circle(screen, (50, 50, 50),
                           dot.position*640,
                           dot.ill_radius*640, width=2)"""
        pygame.draw.circle(screen, COLORS["white"], dot.position * MIN_W_H,
                           dot.radius * MIN_W_H, width=2)

        pygame.draw.line(screen, COLORS["white"], dot.position*MIN_W_H,
                         dot.direction*MIN_W_H, width=2)
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
                dot_controller.mode += 1
            if event.key == pygame.K_n:
                dot_controller.refresh_targets()

    dot_controller.update()

    screen.fill(COLORS["black"])

pygame.quit()
