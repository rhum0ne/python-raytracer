import json
from typing import List, Tuple
from scenes._sceneKeys import *
from objects.sphere_utils import Sphere
from objects.Cube import Cube
from lights.PointLight import PointLight
from lights.DirLight import DirLight
from lights.AmbientLight import AmbientLight
from objects.Plane import Plane
from core.camera import Camera
from animations.SphereScaling import SphereScaling
from animations.LinearMove import LinearMove

class Scene:
    def __init__(self):
        # red_sphere = Sphere(center=(-1, -1, 3), radius=1, color=(255, 0, 0), specular=500, reflective=0.2)
        # blue_sphere = Sphere(center=(1, 0, 4), radius=1, color=(0, 0, 255), specular=500, reflective=0.3)
        
        self.objects = []

        self.lights = []
        
        self.camera = Camera(canvas_width=1200, canvas_height=800)
        self.animation_steps = 1
        
        # self.animations = [
        #     SphereScaling(self, red_sphere, 0.5, 60),
        #     LinearMove(self, blue_sphere, (1, 1, 0), 60)
        # ]
        
        
    def update_frame(self, step):
        for anim in self.animations:
            anim.update_frame(step)
    
    def loadScene(self, filename: str):
        """Load a complete scene from a json file. The file name in parameter can be './dir/file.json', '/dir/file.json', 'dir/file.json', 'file.json', or the same ones without '.json'.

        Args:
            filename (str): the name of the json file
        """
        
        if(not filename.endswith(".json")):
            filename += ".json"
            
        name = filename
        if(filename.startswith("./scenes/") or filename.startswith("/scenes/") or filename.startswith("scenes/")):
            name = filename.split("scenes/")[1]
        
        try:
            print("Loading " + name + "...")
            with open("./scenes/" + name, 'r') as file:
                scene = json.load(file)
            self.parse_scene(scene)
                
        except:
            raise FileNotFoundError("The specified file/path doesn't exists")
    
    def parse_scene(self, scene):
            spheres: List[dict] = scene[OBJECTS][SPHERES]
            planes: List[dict] = scene[OBJECTS][PLANES]
            cubes: List[dict] = scene[OBJECTS][CUBES]
            
            point_lights: List[dict] = scene[LIGHTS][POINTS]
            directional_lights: List[dict] = scene[LIGHTS][DIRECTIONALS]
            ambient_lights: List[dict] = scene[LIGHTS][AMBIENTS]
            
            if len(spheres != 0):
                for sphere in spheres:
                    s: Sphere = self.parseSphere(sphere)
            if len(planes != 0):
                for plane in planes:
                    p: Plane = self.parsePlane(plane)
            if len(cubes != 0):
                for cube in cubes:
                    c: Cube = self.parseCube(plane)
            
            if len(point_lights != 0):
                pass
            if len(directional_lights != 0):
                pass
            if len(ambient_lights != 0):
                pass