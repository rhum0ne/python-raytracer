from utils.maths import dot, sub
import math
from objects.AbstractObject import AbstractObject


class Sphere(AbstractObject):
    def __init__(self, center, radius, color, specular=-1, reflective=0.0):
        super().__init__(color, specular, reflective)
        self.center = center
        self.radius = radius
        self.specular = specular

    def intersect(self, origin, direction):
        return intersect_ray_sphere(origin, direction, self)
    
    def get_normal(self, point):
        N = sub(point, self.center)
        len_sq = dot(N, N)
        if len_sq < 1e-10:
            return (0, 1, 0)
        return (N[0] / (len_sq ** 0.5), N[1] / (len_sq ** 0.5), N[2] / (len_sq ** 0.5))

#O est le point de départ du rayon
#D est la direction du rayon
def intersect_ray_sphere(O, D, sphere: Sphere):
    r = sphere.radius
    CO = sub(O, sphere.center)

    a = dot(D, D)
    
    b = 2.0 * dot(CO, D)
    c = dot(CO, CO) - r*r

    disc = b*b - 4*a*c
    if disc < 0:
        return math.inf
    
    if disc < 1e-10: #Simplifier les cas très proches de 0 et 0 lui même
        return -b / (2*a)

    sqrt_disc = math.sqrt(disc)
    t2 = (-b - sqrt_disc) / (2*a)
    
    if t2 > 0:
        return t2
    
    t1 = (-b + sqrt_disc) / (2*a)
    return t1 if t1 > 0 else math.inf