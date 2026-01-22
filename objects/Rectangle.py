from objects.AbstractObject import AbstractObject
import math
from PIL import Image

from utils.maths import sub

def intersect_cube(origin, direction, center, hl, hw, hh, eps=1e-12):
    vmin = (center[0] - hl, center[1] - hw, center[2] - hh)
    vmax = (center[0] + hl, center[1] + hw, center[2] + hh)

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

class Rectangle(AbstractObject):
        
    def __init__(self, point, length, width, height, color, specular=-1, reflective=0.0, texture=None):
        super().__init__(color, specular, reflective, texture)
        self.center = point
        
        self.length = length
        self.width = width
        self.height = height
        
        self.half_length = length / 2
        self.half_width = width / 2
        self.half_height = height / 2

    def intersect(self, origin, direction, eps=1e-12):
        t = intersect_cube(origin, direction, self.center, self.half_length, self.half_width, self.half_height, eps)
        if t == math.inf:
            return t, self.color

        if self.texture is not None:
            hit_point = (
                origin[0] + direction[0] * t,
                origin[1] + direction[1] * t,
                origin[2] + direction[2] * t
            )
            u, v = self.get_texture_coords(hit_point)

            img = self.texture
            w, h = img.size

            u = u % 1.0
            v = v % 1.0
            px = int(u * (w - 1))
            py = int((1 - v) * (h - 1))
            color = img.getpixel((px, py))
        else:
            color = self.color

        return t, color
    
    
    def get_texture_coords(self, hit_point):
        n = self.get_normal(hit_point)
        x, y, z = hit_point
        cx, cy, cz = self.center
        hl = self.half_length
        hw = self.half_width
        hh = self.half_height
        if abs(n[0]) == 1:
            u = (z - (cz - hl)) / (2 * hl)
            v = (y - (cy - hh)) / (2 * hh)
        elif abs(n[1]) == 1:
            u = (x - (cx - hw)) / (2 * hw)
            v = (z - (cz - hl)) / (2 * hl)
        else:
            u = (x - (cx - hw)) / (2 * hw)
            v = (y - (cy - hh)) / (2 * hh)
            
        if(u > 1): u -= (int(u))
        if(v > 1): v -= (int(v))
        
        return u, v

    def get_normal(self, point):
        n = sub(point, self.center)
        ax, ay, az = abs(n[0]), abs(n[1]), abs(n[2])

        if ax >= ay and ax >= az:
            return (math.copysign(1, n[0]), 0, 0)
        elif ay >= ax and ay >= az:
            return (0, math.copysign(1, n[1]), 0)
        else:
            return (0, 0, math.copysign(1, n[2]))
        
    def get_position(self):
        return self.center

    def set_positions(self, positions):
        # Pour un cube, on attend un seul point (le centre)
        self.center = positions
    
    def get_size(self):
        return self.length