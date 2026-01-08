from utils.maths import dot, sub
import math
from numba import jit
from objects.AbstractObject import AbstractObject


class Sphere(AbstractObject):
    def __init__(self, center, radius, color, specular=-1, reflective=0.0):
        super().__init__(color, specular, reflective)
        self.center = center
        self.radius = radius
        self.radius2 = radius * radius
        self.specular = specular

    def intersect(self, origin, direction):
        return intersect_ray_sphere(origin, direction, self.center, self.radius2)
    
    def get_normal(self, point):
        nx = point[0] - self.center[0]
        ny = point[1] - self.center[1]
        nz = point[2] - self.center[2]
        len_sq = nx*nx + ny*ny + nz*nz
        if len_sq < 1e-10:
            return (0, 1, 0)
        inv_len = 1.0 / math.sqrt(len_sq)
        return (nx * inv_len, ny * inv_len, nz * inv_len)

#O est le point de départ du rayon
#D est la direction du rayon
@jit(nopython=True, cache=True, fastmath=True)
def intersect_ray_sphere(O, D, center, radius2):
    CO = (O[0] - center[0], O[1] - center[1], O[2] - center[2])

    b = 2.0 * (CO[0]*D[0] + CO[1]*D[1] + CO[2]*D[2])
    c = CO[0]*CO[0] + CO[1]*CO[1] + CO[2]*CO[2] - radius2

    disc = b*b - 4*c
    if disc < 0:
        return math.inf
    
    if disc < 1e-1:
        return -b / 2

    sqrt_disc = math.sqrt(disc)
    t2 = (-b - sqrt_disc) / 2
    
    if t2 > 0:
        return t2
    
    t1 = (-b + sqrt_disc) / 2
    return t1 if t1 > 0 else math.inf