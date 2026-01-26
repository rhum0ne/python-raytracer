from utils.maths import length, dot, sub, mul, normalize
import math


def calc_diffuse(normal, L, intensity):
    n_dot_l = dot(normal, L)
    if n_dot_l <= 0:
        return (0, 0, 0)
    
    l_len_sq = dot(L, L)
    if l_len_sq < 1e-10:
        return (0, 0, 0)
    
    l_len = math.sqrt(l_len_sq)
    diffuse = n_dot_l / l_len
    return mul(intensity, diffuse)

def calc_specular(normal, L, ray, intensity, specular):
    n_dot_l = dot(normal, L)
    if n_dot_l <= 0 or specular <= 0:
        return (0, 0, 0)
    R = sub(mul(normal, 2.0 * n_dot_l), L)
    V = mul(ray, -1)
    r_dot_v = dot(R, V)
    if r_dot_v <= 0:
        return (0, 0, 0)
    r_len_sq = dot(R, R)
    v_len_sq = dot(ray, ray)
    if r_len_sq < 1e-10 or v_len_sq < 1e-10:
        return (0, 0, 0)
    denom = math.sqrt(r_len_sq * v_len_sq)
    spec = (r_dot_v / denom) ** specular
    return mul(intensity, spec)

def calcLighting(normal, L, ray, intensity, specular=-1):
    diffuse = calc_diffuse(normal, L, intensity)
    specular_comp = (0, 0, 0)
    if specular > 0:
        specular_comp = calc_specular(normal, L, ray, intensity, specular)
    return (
        max(0.0, min(diffuse[0] + specular_comp[0], 1.0)),
        max(0.0, min(diffuse[1] + specular_comp[1], 1.0)),
        max(0.0, min(diffuse[2] + specular_comp[2], 1.0))
    )