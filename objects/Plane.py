from objects.AbstractObject import AbstractObject
import math

from utils.maths import dot


class Plane(AbstractObject):
    """Plan défini par un point et une normale."""
    
    def __init__(self, point, normal, color, specular=-1, reflective=0, texture=None):
        super().__init__(color, specular, reflective, texture)
        self.point = point
        self.normal = normal
        
        print("Created Plane at point:", self.point, "with normal:", self.normal, "color:", self.color, "reflective:", self.reflective, "texture:", "Yes" if self.texture else "No")
    
    def intersect(self, origin, direction):
        denominator = dot(self.normal, direction)
        if denominator >= 0:
            return math.inf, self.color
        if abs(denominator) < 1e-10:
            return math.inf, self.color
        P_minus_O = (self.point[0] - origin[0], self.point[1] - origin[1], self.point[2] - origin[2])
        numerator = dot(P_minus_O, self.normal)
        t = numerator / denominator
        
        
        hit_point = (
            origin[0] + direction[0] * t,
            origin[1] + direction[1] * t,
            origin[2] + direction[2] * t
        )
        # Texture mapping répétée
        if self.texture is not None:
            img = self.texture
            w, h = img.size
            
            n = self.normal
            abs_n = [abs(x) for x in n]
            if abs_n[0] >= abs_n[1] and abs_n[0] >= abs_n[2]: #Vers X
                u = hit_point[1] - self.point[1]
                v = hit_point[2] - self.point[2]
            elif abs_n[1] >= abs_n[0] and abs_n[1] >= abs_n[2]: #Vers Y
                u = hit_point[0] - self.point[0]
                v = hit_point[2] - self.point[2]
            else: #vers Z
                u = hit_point[0] - self.point[0]
                v = hit_point[1] - self.point[1]
            
            u = u % 1.0 #Pour repeter la texture
            v = v % 1.0
            px = int(u * (w - 1))
            py = int((1 - v) * (h - 1))
            color = img.getpixel((px, py))
        else:
            color = self.color
        return t, color
    
    def get_normal(self, point):
        return self.normal

    def get_position(self):
        return self.point

    def set_positions(self, positions):
        # Pour un plan, on attend un seul point (le point d'ancrage)
        self.point = positions
    
    def get_size(self):
        return None