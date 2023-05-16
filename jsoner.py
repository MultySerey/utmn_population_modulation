import json
import typing

import numpy as np


def sqr_mag(v: np.ndarray) -> float:
    return v[0] ** 2 + v[1] ** 2


def vector_length(v: np.ndarray) -> float:
    return np.sqrt(sqr_mag(v))


def clamp_magnitude(vector: np.ndarray, max_length):
    sqrmag = sqr_mag(vector)
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


class Target:
    def __init__(self):
        self.position = np.random.random(2)

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
        self.position = np.random.random(2)


class TargetList():
    def __init__(self, amount: int) -> None:
        self.target_list: typing.List[Target] = [Dot(i) for i in range(amount)]

    def __len__(self):
        return len(self.target_list)

    def __getitem__(self, item):
        return self.target_list[item]

    def __iter__(self):
        self.iter = 0
        return self

    def __next__(self):
        if self.iter < len(self.target_list):
            out = self.target_list[self.iter]
            self.iter += 1
            return out
        else:
            raise StopIteration


class Dot:
    def __init__(self, id: int) -> None:
        self.id = id
        self.position = np.random.random(2)
        self.velocity = (np.random.random(2)-0.5)*0.5
        self.radius = 0.02
        self.maxSpeed = np.random.random()*0.5
        self.steer_strength = np.random.random()*2+2
        self.ill_radius = 0.04
        self._is_ill = np.around(np.random.random(), decimals=2)
        self.target: Target = Target()
        self.target_num = 0

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
    def is_ill(self):
        return self._is_ill

    @is_ill.setter
    def is_ill(self, value):
        self._is_ill = value
        if self._is_ill < 0:
            self.is_ill = 0
        if self._is_ill > 1:
            self.is_ill = 1

    @property
    def atan2(self):
        return np.arctan2(self.velocity[1], self.velocity[0])

    @property
    def direction(self):
        scale = 0.1
        return np.array([self.x+np.cos(self.atan2)*scale, self.y+np.sin(self.atan2)*scale])  # noqa


class DotController:
    def __init__(self, dot_amount: int, target_amount: int, tick: float):
        self.dot_list: typing.List[Dot] = [Dot(i) for i in range(dot_amount)]
        self.accuracy = 0.025
        self.target_list = TargetList(target_amount)
        self.tick = tick
        self._mode: int = 0
        self.common_target = Target()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value % 3
        print(self._mode)

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

    def is_ill(self, dot: Dot, other: Dot):
        d = vector_length(other.position-dot.position)
        if d < dot.ill_radius+other.ill_radius:
            if other.is_ill:
                dot.is_ill += (dot.is_ill+other.is_ill)*0.01*np.random.random()

    def dot_by_dot_collision(self, dot: Dot, other: Dot):
        dmd = other.position-dot.position
        d = vector_length(dmd)
        if d < dot.radius+other.radius:
            n = dmd/d
            p = (dot.position+other.position)*0.5
            dot.position = p-dot.radius*n
            # другая коллизия
            pv = (2*(dot.velocity[0]*n[0]+dot.velocity[1]*n[1] - other.velocity[0]*n[0]-other.velocity[1]*n[1])) / (dot.steer_strength+other.steer_strength)  # noqa
            dot.velocity -= pv*n*dot.steer_strength*0.5

    def wall_collision(self, dot: Dot):
        if dot.x-dot.radius < 0:
            dot.x = dot.radius
            dot.velocity[0] *= -1

        if dot.y-dot.radius < 0:
            dot.y = dot.radius
            dot.velocity[1] *= -1

        if dot.x+dot.radius > 1:
            dot.x = 1-dot.radius
            dot.velocity[0] *= -1

        if dot.y+dot.radius > 1:
            dot.y = 1-dot.radius
            dot.velocity[1] *= -1

    def update(self):
        for dot in self.dot_list:
            if self.mode != 0:
                distance = vector_length(dot.target.position - dot.position)  # noqa

                if distance < self.accuracy:
                    if self.mode == 1:
                        dot.target.refresh()
                    if self.mode == 2:
                        dot.target = self.common_target
                        self.common_target.refresh()

                desired_direction = normalize(dot.target.position - dot.position)  # noqa

                des_velocity = desired_direction * dot.maxSpeed
                des_steer = (des_velocity - dot.velocity) * dot.steer_strength
                acceleration = np.array(clamp_magnitude(des_steer, dot.steer_strength))  # noqa

                dot.velocity = dot.velocity + acceleration * self.tick

            dot.is_ill -= 0.001

            for dot2 in self.dot_list:
                if not dot2 == dot:
                    self.dot_by_dot_collision(dot, dot2)
                    self.is_ill(dot, dot2)

            dot.x += dot.velocity[0] * self.tick
            dot.y += dot.velocity[1] * self.tick

            self.wall_collision(dot)

    def get(self):
        self.update()
        output: dict = {"count": len(self.dot_list)}
        points: list = []
        for dot in self.dot_list:
            points.append({"id": dot.id,
                           "radius": dot.radius,
                           "x": dot.x,
                           "y": dot.y,
                           "illness": dot.is_ill})
        output["points"] = points

        return json.dumps(output)
