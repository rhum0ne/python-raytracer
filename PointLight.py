from maths import dot, length, sub, mul
from AbstractLight import AbstractLight


class PointLight(AbstractLight):
    def __init__(self, position, intensity):
        super().__init__(intensity)
        self.position = position  # (x, y, z)

    def calcIntensityAtPoint(self, point, normal, ray, specular=-1):

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

        n_dot_l = dot(normal, L)
        if n_dot_l <= 0:
            return (0, 0, 0)
        
        n_len = length(normal)
        l_len = length(L)
        if n_len == 0 or l_len == 0:
            return (0, 0, 0)
        
        diffuse = max(0.0, n_dot_l) / (n_len * l_len)
        total = mul(self.intensity, diffuse)

        if specular != -1:
            R = sub(mul(normal, 2.0 * n_dot_l), L)

            r_dot_v = dot(R, ray)
            if r_dot_v > 0:
                r_len = length(R)
                v_len = length(ray)
                if r_len != 0 and v_len != 0:
                    spec = (r_dot_v / (r_len * v_len)) ** specular
                    specular = mul(self.intensity, spec)
                    total = (total[0] + specular[0], total[1] + specular[1], total[2] + specular[2])

        return total