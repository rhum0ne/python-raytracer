from sphere_utils import Sphere
from PointLight import PointLight
from DirLight import DirLight
from AmbientLight import AmbientLight
from Plane import Plane

class Scene:
    def __init__(self):
        self.objects = [
            Sphere(center=(0, -1, 3), radius=1, color=(255, 0, 0), specular=500),  # Red
            Sphere(center=(2, 0, 4), radius=1, color=(0, 0, 255), specular=500),  # Blue
            Sphere(center=(-2, 0, 4), radius=1, color=(0, 255, 0), specular=10),  # Green
            Plane(point=(0.0, -1.5, 0.0), normal=(0.0, 1.0, 0.0), color=(255, 255, 0))
        ]

        self.lights = [
            PointLight(position=(2.0, 1.0, 2.0), intensity=(0.7, 0.7, 0.7)),
        ]