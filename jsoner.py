import json
import typing

import numpy as np

import setings

ONE_THIRD = 1/3


def vector_length(v: np.ndarray) -> float:
    return np.sqrt(v[0] ** 2 + v[1] ** 2)


def clamp_magnitude(vector: np.ndarray, max_length):
    sqrmag = vector_length(vector)
    if sqrmag > np.abs(max_length):
        vector /= sqrmag
        return vector*max_length
    return vector


def normalize(delta_pos: np.ndarray):
    return delta_pos / vector_length(delta_pos)


class Target:
    def __init__(self, x: float = None, y: float = None):
        if not x and not y:
            self.refresh()
        else:
            self.x = x
            self.y = y

    @property
    def position(self):
        return np.array([self.x, self.y])

    @position.setter
    def position(self, value):
        self.x, self.y = value

    def refresh(self):
        self.position = np.random.random(2)*0.8+0.1


class Dot:
    def __init__(self, id: int, max_speed) -> None:
        self.id = id
        self.position = np.random.random(2)
        self.velocity = (np.random.random(2)-0.5)*0.5
        self.radius = 0.01
        self.max_speed = max_speed
        self.steer_strength = np.random.random()+0.5
        self.ill_radius = 0.02
        self._is_ill = np.around(np.random.random(), decimals=2)
        self.target: Target = Target()
        self.target_num = 0
        self.small_list = None
        self.color = np.random.randint(255, size=3)
        self.trail = np.array([self.position])

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
    def interval_x(self):
        return [self.x-self.radius, self.x+self.radius]

    @property
    def interval_y(self):
        return [self.y-self.radius, self.y+self.radius]

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
        scale = 0.025
        return np.array([self.x+np.cos(self.atan2)*scale, self.y+np.sin(self.atan2)*scale])  # noqa


class DotController:
    def __init__(self, dot_amount: int, tick: float, mode: int = 0, max_speed: float = 0.5, target_num: int = 7):
        self.dot_list: typing.List[Dot] = [
            Dot(i, max_speed) for i in range(dot_amount)]
        self.accuracy = 0.05
        self.tick = tick
        self._mode: int = mode
        self.common_target = Target()
        self.target_num = target_num
        self.ticker = 0
        pi_over_num = np.pi/self.target_num
        self.target_list = [
            Target(np.cos(pi_over_num*i*2+1)*ONE_THIRD+0.5,
                   np.sin(pi_over_num*i*2+1)*ONE_THIRD+0.5) for i in range(self.target_num)]  # noqa
        for dot in self.dot_list:
            self.small_list(dot)

    def set_speed(self, input_speed):
        for dot in self.dot_list:
            dot.max_speed = input_speed

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        total_modes = 6
        self._mode = value % total_modes
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

    # заражение
    def is_ill(self, dot: Dot, other: Dot):
        d = vector_length(other.position-dot.position)
        if d < dot.ill_radius+other.ill_radius:
            if other.is_ill:
                dot.is_ill += (dot.is_ill+other.is_ill) * 0.025*np.random.random()  # noqa

    # коллизия между точками
    def dot_by_dot_collision(self, dot: Dot, other: Dot):
        dmd = other.position-dot.position
        d = vector_length(dmd)
        if d < dot.radius+other.radius:
            n = dmd/d
            p = (dot.position+other.position)*0.5
            dot.position = p-dot.radius*n
            # изменение скорости
            pv = (2*(dot.velocity[0]*n[0]+dot.velocity[1]*n[1] - other.velocity[0]*n[0]-other.velocity[1]*n[1])) / (dot.steer_strength+other.steer_strength)  # noqa
            dot.velocity -= pv*n*dot.steer_strength*0.5

    # коллизия с границами области
    def wall_collision(self, dot: Dot):
        if dot.x-dot.radius < 0:
            dot.x = dot.radius
            if self.mode == 0:
                dot.velocity[0] *= -1

        if dot.y-dot.radius < 0:
            dot.y = dot.radius
            if self.mode == 0:
                dot.velocity[1] *= -1

        if dot.x+dot.radius > 1:
            dot.x = 1-dot.radius
            if self.mode == 0:
                dot.velocity[0] *= -1

        if dot.y+dot.radius > 1:
            dot.y = 1-dot.radius
            if self.mode == 0:
                dot.velocity[1] *= -1

    # выбор точек для режима "регулярное посещение заданных точек"
    def small_list(self, dot: Dot):
        dot.small_list = np.random.choice(self.target_list, 2, False)

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

    def update(self):
        for dot in self.dot_list:
            if self.ticker % 600 == 0:
                self.small_list(dot)

            if self.mode != 0:
                distance = vector_length(dot.target.position - dot.position)  # noqa

                if distance+dot.radius < self.accuracy:
                    if self.mode == 1:
                        dot.target = Target()
                    if self.mode == 2:
                        dot.target = self.common_target
                        self.common_target.refresh()
                    if self.mode == 3:
                        dot.target = np.random.choice(self.target_list)
                    if self.mode == 4:
                        dot.target_num += 1
                        dot.target = self.target_list[dot.target_num % len(self.target_list)]  # noqa
                    if self.mode == 5:
                        dot.target_num += 1
                        dot.target = dot.small_list[dot.target_num % len(dot.small_list)]  # noqa

                desired_direction = normalize(dot.target.position - dot.position)  # noqa

                des_velocity = desired_direction * dot.max_speed
                des_steer = (des_velocity - dot.velocity) * dot.steer_strength
                acceleration = clamp_magnitude(des_steer, dot.steer_strength)  # noqa

                dot.velocity += acceleration * self.tick

            dot.is_ill -= 0.005
            dot.position += dot.velocity * self.tick
            if setings.WALL_COLLISION:
                self.wall_collision(dot)
            dot.trail = np.append(dot.trail, [dot.position], axis=0)

        over = self.overlaps()
        if over:
            for i in over:
                dot = self.dot_list[i]
                for k in over:
                    dot2 = self.dot_list[k]
                    if not dot2 == dot:
                        if setings.DOT_BY_DOT_COLLISION:
                            self.dot_by_dot_collision(dot, dot2)
                        self.is_ill(dot, dot2)

        self.ticker += 1

    def get(self):
        self.update()
        output: dict = {"count": len(self.dot_list)}
        output["target_radius"] = self.accuracy
        if self.mode < 2:
            output["target"] = [[-1, -1]]
        if self.mode == 2:
            output["target"] = [self.common_target.position.tolist()]
        if self.mode > 2:
            output["target"] = [t.position.tolist() for t in self.target_list]
        output["points"] = [{"id": dot.id,
                             "radius": dot.radius,
                             "x": dot.x,
                             "y": dot.y,
                             "illness": dot.is_ill
                             } for dot in self.dot_list]
        return json.dumps(output)
