import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

# Задаём количество точек

count = 50
global xlimer, ylimer

xlimer = 15
ylimer = 15


def generate_vel():
    return (np.random.random_sample() - 0.5)/4


def move():
    global dots
    for i in range(len(dots)):
        velx = generate_vel()
        vely = generate_vel()
        x = dots[i][0]+velx
        y = dots[i][1]+vely

        # Делаем ограничения для точек, чтобы они не выходили за пределы границы
        if x >= xlimer:
            x = xlimer
            velx = -1*velx
        if x <= 0:
            x = 0
            velx = -1*velx
        if y >= ylimer:
            y = ylimer
            vely = -1*vely
        if y <= 0:
            y = 0
            vely = -1*vely
        dots[i] = (x, y)
        # dots[i][0] = x
        # dots[i][1] = y


fig = plt.figure()
ax = plt.axes(xlim=(0, xlimer), ylim=(0, ylimer))

dots = [(5, 5)]*count

x, y = zip(*dots)
d, = ax.plot(x, y, 'ro')


def animate(i):
    global dots
    move()
    x, y = zip(*dots)
    d.set_data(x, y)
    return d,


anim = animation.FuncAnimation(fig, animate, frames=1000, interval=20)

plt.show()
