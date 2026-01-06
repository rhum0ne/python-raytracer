from maths import dot, length, sub, mul

class PointLight:
    def __init__(self, position, intensity):
        self.position = position  # (x, y, z)
        self.intensity = intensity  # (r, g, b) Car moi je veux de la couleur :D


    def calcIntensityAtPoint(self, point, normal):
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
