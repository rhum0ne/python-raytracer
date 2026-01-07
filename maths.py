import math

import numpy
def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def add(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def mul(a, k: float):
    return (a[0]*k, a[1]*k, a[2]*k)


def normalize(v):
    return mul(v, 1.0 / length(v))

def length(v):
    return numpy.sqrt(dot(v, v))

