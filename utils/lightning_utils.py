from utils.maths import length, dot, sub, mul


def calcLighting(normal, L, ray, intensity, specular=-1):
    n_dot_l = dot(normal, L)
    if n_dot_l <= 0:
        return (0, 0, 0)
    
    l_len_sq = dot(L, L)
    if l_len_sq < 1e-10:
        return (0, 0, 0)
    
    l_len = l_len_sq ** 0.5
    diffuse = n_dot_l / l_len
    total = mul(intensity, diffuse)

    if specular > 0:
        R = sub(mul(normal, 2.0 * n_dot_l), L)
        V = mul(ray, -1)
        r_dot_v = dot(R, V)
        if r_dot_v > 0:
            r_len_sq = dot(R, R)
            v_len_sq = dot(ray, ray)
            if r_len_sq > 1e-10 and v_len_sq > 1e-10:
                denom = (r_len_sq * v_len_sq) ** 0.5
                spec = (r_dot_v / denom) ** specular
                specular_pow = mul(intensity, spec)
                total = (total[0] + specular_pow[0], total[1] + specular_pow[1], total[2] + specular_pow[2])

    return total