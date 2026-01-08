import math
from numba import jit

@jit(nopython=True, cache=True, fastmath=True)
def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

@jit(nopython=True, cache=True, fastmath=True)
def sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

@jit(nopython=True, cache=True, fastmath=True)
def add(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

@jit(nopython=True, cache=True, fastmath=True)
def mul(a, k):
    return (a[0]*k, a[1]*k, a[2]*k)

@jit(nopython=True, cache=True, fastmath=True)
def normalize(v):
    len_sq = v[0]*v[0] + v[1]*v[1] + v[2]*v[2]
    if len_sq < 1e-10:
        return (0.0, 0.0, 0.0)
    if len_sq == 1.0:
        return v
    inv_len = 1.0 / math.sqrt(len_sq)
    return (v[0]*inv_len, v[1]*inv_len, v[2]*inv_len)

@jit(nopython=True, cache=True, fastmath=True)
def length(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])

