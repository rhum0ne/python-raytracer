from AbstractLight import AbstractLight
from maths import dot, length, mul


class DirLight(AbstractLight):
    
    def __init__(self, direction, intensity):
        super().__init__(intensity)
        self.direction = direction 
    
    def calcIntensityAtPoint(self, point, normal, ray, specular=-1):
        #Je sais pas pourquoi ca marche, mais ca marche, 
        N_dot_Dir = dot(normal, self.direction);
        if( N_dot_Dir >= 0):
            return (0, 0, 0)
        
        n_len = length(normal)
        l_len = length(self.direction)
        if n_len == 0 or l_len == 0:
            return (0, 0, 0)
        
        return mul(self.intensity, -N_dot_Dir / (l_len * n_len))