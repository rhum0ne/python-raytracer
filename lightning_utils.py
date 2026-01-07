from maths import length, dot, sub, mul


def calcLighting(normal, L, ray, intensity, specular=-1):
    n_dot_l = dot(normal, L)
    if n_dot_l <= 0:
        return (0, 0, 0)
        
    l_len = length(L)
    if l_len == 0:
        return (0, 0, 0)
        
    diffuse = max(0.0, n_dot_l) / (l_len)
    total = mul(intensity, diffuse)

    if specular != -1:
        R = sub(mul(normal, 2.0 * n_dot_l), L)
        V = mul(ray, -1)
        r_dot_v = dot(R, V)
        if r_dot_v > 0:
            r_len = length(R)
            v_len = length(ray)
            if r_len != 0 and v_len != 0:
                spec = (r_dot_v / (r_len * v_len)) ** specular
                specular_pow = mul(intensity, spec)
                total = (total[0] + specular_pow[0], total[1] + specular_pow[1], total[2] + specular_pow[2])

    return total