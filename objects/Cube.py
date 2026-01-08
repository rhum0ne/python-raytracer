from objects.AbstractObject import AbstractObject
import math

from utils.maths import sub

def intersect_cube(origin, direction, center, half_length, eps=1e-12):
    vmin = (center[0] - half_length, center[1] - half_length, center[2] - half_length)
    vmax = (center[0] + half_length, center[1] + half_length, center[2] + half_length)

    ox, oy, oz = origin
    dx, dy, dz = direction

    tmin = -math.inf
    tmax = math.inf

    for i in range(3):
        if i == 0:
            o, d, mn, mx = ox, dx, vmin[0], vmax[0]
        elif i == 1:
            o, d, mn, mx = oy, dy, vmin[1], vmax[1]
        else:
            o, d, mn, mx = oz, dz, vmin[2], vmax[2]
        
        if abs(d) < eps:
            if o < mn or o > mx:
                return math.inf
            continue

        inv = 1.0 / d
        t1 = (mn - o) * inv
        t2 = (mx - o) * inv
        if t1 > t2:
            t1, t2 = t2, t1

        tmin = max(tmin, t1)
        tmax = min(tmax, t2)

        if tmin > tmax:
            return math.inf

    if tmax < 0.0:
        return math.inf

    return max(tmin, 0.0)

class Cube(AbstractObject):
    def __init__(self, point, length, color, specular=-1, reflective=0.0):
        super().__init__(color, specular, reflective)
        self.center = point
        self.length = length
        self.half_length = length / 2

    def intersect(self, origin, direction, eps=1e-12):
        return intersect_cube(origin, direction, self.center, self.half_length, eps)

    def get_normal(self, point):
        n = sub(point, self.center)
        ax, ay, az = abs(n[0]), abs(n[1]), abs(n[2])

        if ax >= ay and ax >= az:
            return (math.copysign(1, n[0]), 0, 0)
        elif ay >= ax and ay >= az:
            return (0, math.copysign(1, n[1]), 0)
        else:
            return (0, 0, math.copysign(1, n[2]))