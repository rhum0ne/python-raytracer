from lights.AbstractLight import AbstractLight
from utils.maths import dot, length, mul


class AmbientLight(AbstractLight):
    
    def __init__(self, intensity):
        super().__init__(intensity)
    
    def calcIntensityAtPoint(self, point, normal, ray, specular=-1):
        return self.intensity

    def get_direction_from_point(self, point):
        return None