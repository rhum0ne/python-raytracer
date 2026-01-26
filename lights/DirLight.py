from lights.AbstractLight import AbstractLight
from utils.lightning_utils import calcLighting
from utils.maths import mul

class DirLight(AbstractLight):
    
    def __init__(self, direction, intensity):
        super().__init__(intensity)
        self.direction = mul(direction, -1)
        
        print("Created Directional Light with direction:", self.direction, "and intensity:", self.intensity)
    
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