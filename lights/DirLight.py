from lights.AbstractLight import AbstractLight
from utils.lightning_utils import calcLighting
from utils.maths import normalize

class DirLight(AbstractLight):
    
    def __init__(self, direction, intensity):
        super().__init__(intensity)
        # Normaliser la direction une seule fois au démarrage
        self.direction = normalize(direction)
    
    def calcIntensityAtPoint(self, point, normal, ray, specular=-1):
        return calcLighting(
            normal=normal,
            L=self.direction,
            ray=ray,
            intensity=self.intensity,
            specular=specular
        )
    
    def get_direction_from_point(self, point):
        return self.direction