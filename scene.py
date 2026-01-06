from sphere_utils import Sphere
from PointLight import PointLight

class Scene:
    def __init__(self):
        self.spheres = [
            Sphere(center=(0.0, 2.5, 6.0), radius=1, color=(255, 255, 0)),
            Sphere(center=(0.0, 1, 6.0), radius=1, color=(255, 255, 0)),
            Sphere(center=(0.0, -0.5, 6.0), radius=1, color=(255, 255, 0)),
            Sphere(center=(-1.0, -1.5, 6.0), radius=1.2, color=(0, 0, 255)),
            Sphere(center=(1.0,-1.5, 6.0), radius=1.2, color=(0, 255, 0)),
        ]

        self.lights = [
            PointLight(position=(2.0, 2.0, 1.0), intensity=(1, 1, 1)),
            PointLight(position=(0.0, 0.0, 4.0), intensity=(1.0, 1.0, 1.0)),
        ]