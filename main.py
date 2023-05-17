import pygame
from numpy import around as nparound

from jsoner import DotController

WIDTH, HEIGHT = 640, 640
MIN_W_H = min(WIDTH, HEIGHT)
FPS = 60
TICK = 1/FPS

COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
}


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


TARGET = False
dot_controller = DotController(100, TICK)

running = True


def redraw_window():
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, MIN_W_H, MIN_W_H), 1)
    if dot_controller.mode == 2:
        pygame.draw.circle(screen, COLORS["green"],
                           dot_controller.common_target.position*MIN_W_H,
                           dot_controller.accuracy*MIN_W_H, 1)
    if dot_controller.mode >= 3:
        for target in dot_controller.target_list:
            pygame.draw.circle(screen, COLORS["green"],
                               target.position*MIN_W_H,
                               dot_controller.accuracy*MIN_W_H, 1)
    for dot in dot_controller:
        """if dot_controller.mode == 1:
            pygame.draw.circle(screen, COLORS["green"],
                               dot.target.position*MIN_W_H,
                               dot_controller.accuracy*MIN_W_H, 1)"""
        if dot.is_ill:
            red_col = int(nparound(200*dot.is_ill))
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


while running:
    clock.tick(FPS)
    redraw_window()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                dot_controller.mode = 0
            if event.key == pygame.K_1:
                dot_controller.mode = 1
            if event.key == pygame.K_2:
                dot_controller.mode = 2
            if event.key == pygame.K_3:
                dot_controller.mode = 3
            if event.key == pygame.K_4:
                dot_controller.mode = 4
            if event.key == pygame.K_5:
                dot_controller.mode = 5

    dot_controller.update()
    screen.fill(COLORS["black"])

pygame.quit()
