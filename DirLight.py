from AbstractLight import AbstractLight
from maths import dot, length, mul


class DirLight(AbstractLight):
    
    def __init__(self, direction, intensity):
        super().__init__(intensity)
        self.direction = direction 
    
    def calcIntensityAtPoint(self, point, normal):
        #Je sais pas pourquoi ca marche, mais ca marche, 
        if(dot(normal, self.direction) >= 0):
            return (0, 0, 0)
        
        return mul(self.intensity, -dot(normal, self.direction) / (length(self.direction) * length(normal)))
