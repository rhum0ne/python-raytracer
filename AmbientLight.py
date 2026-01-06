from AbstractLight import AbstractLight
from maths import dot, length, mul


class AmbientLight(AbstractLight):
    
    def __init__(self, intensity):
        super().__init__(intensity)
    
    def calcIntensityAtPoint(self, point, normal):
        return self.intensity
