from maths import dot, length, sub, mul
from AbstractLight import AbstractLight
from lightning_utils import calcLighting

class PointLight(AbstractLight):
    def __init__(self, position, intensity):
        super().__init__(intensity)
        self.position = position  # (x, y, z)

    def calcIntensityAtPoint(self, point, normal, ray, specular=-1):
        L = sub(self.position, point)
        return calcLighting(
            normal=normal,
            L=L,
            ray=ray,
            intensity=self.intensity,
            specular=specular
        )
    
    def get_direction_from_point(self, point):
        return sub(self.position, point)