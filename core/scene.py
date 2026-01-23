import json
from utils.scene_parser import SceneParser
from typing import List, Tuple
from objects.sphere_utils import Sphere
from objects.Cube import Cube
from lights.PointLight import PointLight
from lights.DirLight import DirLight
from lights.AmbientLight import AmbientLight
from objects.Plane import Plane
from core.camera import Camera
from animations.Scaling import Scaling
from animations.LinearMove import LinearMove

class Scene:
    def __init__(self):
        self.scene_parser = SceneParser(self)
        self.objects = []

        self.lights = []
        
        self.camera = Camera(canvas_width=1200, canvas_height=800)
        self.animation_steps = 1
        
        self.animations = []
        
        
    def update_frame(self, step):
        for anim in self.animations:
            anim.update_frame(step)
    
    def loadScene(self, filename: str):
        """Load a complete scene from a json file. The file name in parameter can be './dir/file.json', '/dir/file.json', 'dir/file.json', 'file.json', or the same ones without '.json'.

        Args:
            filename (str): the name of the json file
        """
        if(filename == None):
            self.loadDefaultScene()
            return
        
        if(not filename.endswith(".json")):
            filename += ".json"
            
        name = filename
        if(filename.startswith("./scenes/") or filename.startswith("/scenes/") or filename.startswith("scenes/")):
            name = filename.split("scenes/")[1]
        
        scene = None
        try:
            print("Loading " + name + "...")
            with open("./scenes/" + name, 'r') as file:
                scene = json.load(file)
                
        except:
            raise FileNotFoundError("The specified file/path doesn't exists")
        
        self.scene_parser.parse_scene(scene)
        #print(f"Scene noaded \n\tobjects : {self.objects}\n\tlights : {self.lights}\n\tanimations : {self.animations}")

    def loadDefaultScene(self):
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
        self.animation_steps = 1
        
        self.animations = [
            LinearMove(self, blue_sphere, (1, 1, 0), 60)
        ] 

    
    def add_object(self, obj):
        self.objects.append(obj)

    def add_light(self, light):
        self.lights.append(light)
    
    def add_animation(self, animation):
        self.animations.append(animation)