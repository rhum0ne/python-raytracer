from objects.AbstractObject import AbstractObject
import math
from numba import jit

from utils.maths import dot

@jit(nopython=True, cache=True, fastmath=True)
def intersect_plane(origin, direction, plane_point, plane_normal):
    denominator = plane_normal[0]*direction[0] + plane_normal[1]*direction[1] + plane_normal[2]*direction[2]
    
    if denominator >= 0:
        return math.inf
    
    if abs(denominator) < 1e-10:
        return math.inf
    
    P_minus_O = (plane_point[0] - origin[0], plane_point[1] - origin[1], plane_point[2] - origin[2])
    numerator = P_minus_O[0]*plane_normal[0] + P_minus_O[1]*plane_normal[1] + P_minus_O[2]*plane_normal[2]
    return numerator / denominator


class Plane(AbstractObject):
    """Plan défini par un point et une normale."""
    
    def __init__(self, point, normal, color, specular=-1, reflective=0.0):
        super().__init__(color, specular, reflective)
        self.point = point
        self.normal = normal
    
    def intersect(self, origin, direction):
        return intersect_plane(origin, direction, self.point, self.normal)
    
    def get_normal(self, point):
        return self.normal
