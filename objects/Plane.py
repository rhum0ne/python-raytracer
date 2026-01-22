from objects.AbstractObject import AbstractObject
import math

from utils.maths import dot


class Plane(AbstractObject):
    """Plan défini par un point et une normale."""
    
    def __init__(self, point, normal, color, specular=-1, reflective=0.0):
        super().__init__(color, specular, reflective)
        self.point = point
        self.normal = normal
    
    def intersect(self, origin, direction):
        denominator = dot(self.normal, direction)
        
        if denominator >= 0:
            return math.inf
        
        if abs(denominator) < 1e-10:
            return math.inf
        
        P_minus_O = (self.point[0] - origin[0], self.point[1] - origin[1], self.point[2] - origin[2])
        numerator = dot(P_minus_O, self.normal)
        return numerator / denominator
    
    def get_normal(self, point):
        return self.normal

    def get_position(self):
        return self.point
    
    def get_size(self):
        return None