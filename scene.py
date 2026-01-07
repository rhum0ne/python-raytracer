from sphere_utils import Sphere
from PointLight import PointLight
from DirLight import DirLight
from AmbientLight import AmbientLight
from Plane import Plane

class Scene:
    def __init__(self):
        self.objects = [
            Sphere(center=(-2.0, 0, 10.0), radius=1.2, color=(0, 0, 255), specular=500),
            Sphere(center=(1.0,-1, 6.0), radius=1.2, color=(0, 255, 0), specular=1000),
            Plane(point=(0.0, -1.5, 0.0), normal=(0.0, 1.0, 0.0), color=(255, 255, 0)),
        ]

        self.lights = [
            PointLight(position=(2.0, 2.0, 1.0), intensity=(1, 1, 1)),
            PointLight(position=(0.0, 1.0, 4.0), intensity=(1.0, 1.0, 1.0)),
            DirLight(direction=(0, -1, 1), intensity=(1,1, 1)),
            AmbientLight(intensity=(0.2, 0.2, 0.4))
        ]