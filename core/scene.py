from objects.sphere_utils import Sphere
from lights.PointLight import PointLight
from lights.DirLight import DirLight
from lights.AmbientLight import AmbientLight
from objects.Plane import Plane
from core.camera import Camera
from animations.SphereScaling import SphereScaling
from animations.LinearMove import LinearMove

class Scene:
    def __init__(self):
        red_sphere = Sphere(center=(-1, -1, 3), radius=1, color=(255, 0, 0), specular=500, reflective=0.2)
        blue_sphere = Sphere(center=(1, 0, 4), radius=1, color=(0, 0, 255), specular=500, reflective=0.3)
        
        self.objects = [
            red_sphere,
            blue_sphere,
            Sphere(center=(-2, 0, 4), radius=1, color=(0, 255, 0), specular=10, reflective=0.4),
            Plane(point=(0.0, -1.5, 0.0), normal=(0.0, 1.0, 0.0), color=(255, 255, 0), reflective=0.1)
        ]

        self.lights = [
            PointLight(position=(2.0, 1.0, 2.0), intensity=(0.7, 0.7, 0.7)),
            DirLight(direction=(-1.0, -1.0, 1.0), intensity=(0.2, 0.2, 0.2)),
            AmbientLight(intensity=(0.2, 0.2, 0.2))
        ]
        
        self.camera = Camera(canvas_width=1200, canvas_height=800)
        self.animation_steps = 60
        
        self.animations = [
            SphereScaling(self, red_sphere, 0.5, 60),
            LinearMove(self, blue_sphere, (1, 1, 0), 60)
        ] 
        
        
    def update_frame(self, step):
        for anim in self.animations:
            anim.update_frame(step)