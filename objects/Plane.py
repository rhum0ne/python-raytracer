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
        
        if abs(denominator) < 1e-10:
            return math.inf
        
        if denominator >= 0:
            return math.inf
        
        #La distance d'intersection d'une droite avec un plan est: t = ((P0 - O) . N) / (D . N)
        #P0 est un point du plan
        #O est l'origine du rayon
        #N est la normale du plan
        #D est la direction du rayon
        P_moins_O = (
            self.point[0] - origin[0],
            self.point[1] - origin[1],
            self.point[2] - origin[2],
        )
        numerator = dot(P_moins_O, self.normal)
        return numerator / denominator
    
    def get_normal(self, point):
        return self.normal
