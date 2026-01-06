from maths import dot, sub
import math

class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color  # (r,g,b)

#O est le point de départ du rayon
#D est la direction du rayon
def intersect_ray_sphere(O, D, sphere: Sphere):
    # returns (inf, inf) if no hit
    r = sphere.radius
    CO = sub(O, sphere.center)

    a = dot(D, D)
    b = 2.0 * dot(CO, D)
    c = dot(CO, CO) - r*r

    disc = b*b - 4*a*c
    if disc < 0:
        return math.inf
    
    if(disc == 0):
        return -b / (2*a)

    sqrt_disc = math.sqrt(disc)
    t1 = (-b + sqrt_disc) / (2*a)
    t2 = (-b - sqrt_disc) / (2*a)

    return min(t1, t2)
