from maths import dot, length, sub, mul
from AbstractLight import AbstractLight


class PointLight(AbstractLight):
    def __init__(self, position, intensity):
        super().__init__(intensity)
        self.position = position  # (x, y, z)

    def calcIntensityAtPoint(self, point, normal):

        #Ce sera peut être utile plus tard pour faire une atténuation
        #distances = (
        #    point[0] - self.position[0],
        #    point[1] - self.position[1],
        #    point[2] - self.position[2],
        #)

        #distance_squared = distances[0]**2 + distances[1]**2 + distances[2]**2

        #if distance_squared == 0:
        #    return self.intensity 
        
        L = sub(self.position, point)
        if(dot(normal, L) <= 0):
            return (0, 0, 0)
        return mul(self.intensity, max(0, dot(normal, L)) / (length(L) * length(normal)))
