from typing import List, Tuple
from objects.Cube import Cube
from objects.sphere_utils import Sphere
from objects.Plane import Plane
from lights.PointLight import PointLight
from lights.DirLight import DirLight
from lights.AmbientLight import AmbientLight
from animations.Scaling import Scaling
from animations.LinearMove import LinearMove
from utils._sceneKeys import *

class SceneParser:
    def __init__(self, scene):
        from core.scene import Scene
        self.scene: Scene = scene
        
    def parse_scene(self, jsonfile):
        """Parse the scene described in the json file parameter.

        Args:
            jsonfile (json file): the scene json file to parse
        """
        spheres: List[dict] = jsonfile[OBJECTS][SPHERES]
        planes: List[dict] = jsonfile[OBJECTS][PLANES]
        cubes: List[dict] = jsonfile[OBJECTS][CUBES]
        
        point_lights: List[dict] = jsonfile[LIGHTS][POINTS]
        directional_lights: List[dict] = jsonfile[LIGHTS][DIRECTIONALS]
        ambient_lights: List[dict] = jsonfile[LIGHTS][AMBIENTS]
        
        if len(spheres) != 0:
            for sphere in spheres:
                s: Sphere = self.parse_sphere(sphere)
                self.scene.add_object(s)
        if len(planes) != 0:
            for plane in planes:
                p: Plane = self.parse_plane(plane)
                self.scene.add_object(p)
        if len(cubes) != 0:
            for cube in cubes:
                c: Cube = self.parse_cube(cube)
                self.scene.add_object(c)
        
        if len(point_lights) != 0:
            for p_light in point_lights:
                pl: PointLight = self.parse_point_light(p_light)
                self.scene.add_light(pl)
        if len(directional_lights) != 0:
            for d_light in directional_lights:
                dl: DirLight = self.parse_directional_light(d_light)
                self.scene.add_light(dl)
        if len(ambient_lights) != 0:
            for a_light in ambient_lights:
                al: AmbientLight = self.parse_ambient_light(a_light)
                self.scene.add_light(al)
    
    def parse_sphere(self, sphere: dict) -> Sphere:
        x, y, z = sphere[SPHERES_CENTER][SPHERES_CENTER_X], sphere[SPHERES_CENTER][SPHERES_CENTER_Y], sphere[SPHERES_CENTER][SPHERES_CENTER_Z]
        radius = sphere[SPHERES_RADIUS]
        r, g, b = sphere[SPHERES_COLOR][SPHERES_COLOR_R],sphere[SPHERES_COLOR][SPHERES_COLOR_G], sphere[SPHERES_COLOR][SPHERES_COLOR_B]
        specular = sphere[SPHERES_SPECULAR]
        reflective = sphere[SPHERES_REFLECTIVE]
        
        s = Sphere((x, y, z), radius, (r, g, b), specular, reflective)
        if len(sphere[ANIMATIONS]) != 0:
            self.parse_animations(sphere, s)
        return s
    
    def parse_plane(self, plane: dict) -> Sphere:
        x, y, z = plane[PLANES_POINT][PLANES_POINT_X], plane[PLANES_POINT][PLANES_POINT_Y], plane[PLANES_POINT][PLANES_POINT_Z]
        normal = (plane[PLANES_NORMAL][PLANES_NORMAL_X], plane[PLANES_NORMAL][PLANES_NORMAL_Y], plane[PLANES_NORMAL][PLANES_NORMAL_Z])
        r, g, b = plane[PLANES_COLOR][PLANES_COLOR_R],plane[PLANES_COLOR][PLANES_COLOR_G], plane[PLANES_COLOR][PLANES_COLOR_B]
        reflective = plane[PLANES_REFLECTIVE]
        
        p = Plane((x, y, z), normal, (r, g, b), reflective)
        return p
    
    def parse_cube(self, cube: dict) -> Cube:
        x, y, z = cube[CUBES_POINT][CUBES_POINT_X], cube[CUBES_POINT][CUBES_POINT_Y], cube[CUBES_POINT][CUBES_POINT_Z]
        radius = cube[CUBES_LENGTH]
        r, g, b = cube[CUBES_COLOR][CUBES_COLOR_R],cube[CUBES_COLOR][CUBES_COLOR_G], cube[CUBES_COLOR][CUBES_COLOR_B]
        specular = cube[CUBES_SPECULAR]
        reflective = cube[CUBES_REFLECTIVE]
        
        c = Cube((x, y, z), radius, (r, g, b), specular, reflective)
        if len(cube[ANIMATIONS]) != 0:
            self.parse_animations(cube, c)
        return c
    
    def parse_point_light(self, light: dict) -> PointLight:
        x, y, z = light[POINTS_POSITION][POINTS_POSITION_X], light[POINTS_POSITION][POINTS_POSITION_Y], light[POINTS_POSITION][POINTS_POSITION_Z]
        r, g, b = light[POINTS_INTENSITY][POINTS_INTENSITY_R],light[POINTS_INTENSITY][POINTS_INTENSITY_G], light[POINTS_INTENSITY][POINTS_INTENSITY_B]
        return PointLight((x, y, z), (r, g, b))
    
    def parse_directional_light(self, light: dict) -> DirLight:
        x, y, z = light[DIRECTIONALS_DIRECTION][DIRECTIONALS_DIRECTION_X], light[DIRECTIONALS_DIRECTION][DIRECTIONALS_DIRECTION_Y], light[DIRECTIONALS_DIRECTION][DIRECTIONALS_DIRECTION_Z]
        r, g, b = light[DIRECTIONALS_INTENSITY][DIRECTIONALS_INTENSITY_R],light[DIRECTIONALS_INTENSITY][DIRECTIONALS_INTENSITY_G], light[DIRECTIONALS_INTENSITY][DIRECTIONALS_INTENSITY_B]
        return DirLight((x, y, z), (r, g, b))
    
    def parse_ambient_light(self, light: dict) -> AmbientLight:
        r, g, b = light[AMBIENTS_INTENSITY][AMBIENTS_INTENSITY_R],light[AMBIENTS_INTENSITY][AMBIENTS_INTENSITY_G], light[AMBIENTS_INTENSITY][AMBIENTS_INTENSITY_B]
        return AmbientLight((r, g, b))
    
    def parse_animations(self, object_dict: dict, object) :
        for anim in object_dict[ANIMATIONS]:
            steps = anim[ANIMATIONS_STEPS]
            match anim[ANIMATIONS_TYPE]:
                case "scale":
                    size = anim[ANIMATIONS_SIZE]
                    self.scene.add_animation(Scaling(self.scene, object, size, steps))
                case "linear":
                    target = (anim[ANIMATIONS_LINEAR_TARGET][ANIMATIONS_LINEAR_X], anim[ANIMATIONS_LINEAR_TARGET][ANIMATIONS_LINEAR_Y], anim[ANIMATIONS_LINEAR_TARGET][ANIMATIONS_LINEAR_Z])
                    self.scene.add_animation(LinearMove(self.scene, object, target, steps))