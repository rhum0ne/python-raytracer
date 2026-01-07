import math

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def add(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def mul(a, k: float):
    return (a[0]*k, a[1]*k, a[2]*k)


def normalize(v):
    len_sq = dot(v, v)
    if len_sq < 1e-10:
        return (0, 0, 0)
    return mul(v, 1.0 / (len_sq ** 0.5))

def length(v):
    return math.sqrt(dot(v, v))

