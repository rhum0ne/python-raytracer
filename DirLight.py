from AbstractLight import AbstractLight
from maths import dot, length, mul, sub


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
        
        diffuse = max(0.0, N_dot_Dir) / (n_len * l_len)
        total = mul(self.intensity, diffuse)
        
        if specular != -1:
            R = sub(mul(normal, 2.0 * N_dot_Dir), self.direction)

            r_dot_v = dot(R, ray)
            if r_dot_v > 0:
                r_len = length(R)
                v_len = length(ray)
                if r_len != 0 and v_len != 0:
                    spec = (r_dot_v / (r_len * v_len)) ** specular
                    specular = mul(self.intensity, spec)
                    total = (total[0] + specular[0], total[1] + specular[1], total[2] + specular[2])

        return total