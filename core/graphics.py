import math
import os
from datetime import datetime
from multiprocessing import Pool, cpu_count

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Pillow manquant. Installe-le avec: pip install pillow")
from core.camera import Camera
from core.scene import Scene
from utils.maths import mul, sub, dot, normalize, add, length
from skybox import Skybox
from skybox import gradient_sky
from gifs import save_gif

sky = Skybox("sky.jpg")

def closest_intersection(O, D, t_min, t_max, objects):
    closest_t = math.inf
    closest_object = None

    for obj in objects:
        intersection = obj.intersect(O, D)

        if t_min <= intersection < closest_t and intersection <= t_max:
            closest_t = intersection
            closest_object = obj

    return closest_object, closest_t

def compute_lighting(point, normal, ray, closest_object, lights, objects, t_max, t_min=0.001):
    intensity_r = 0.0
    intensity_g = 0.0
    intensity_b = 0.0
    
    normal_offset = mul(normal, 0.001)
    shadow_origin = (point[0] + normal_offset[0], point[1] + normal_offset[1], point[2] + normal_offset[2])
    
    for l in lights:
        dir = l.get_direction_from_point(point)
        if dir is None:
            continue
        
        dir_length = length(dir)
        if dir_length < 1e-10:
            continue
        
        dir_normalized = normalize(dir)
        
        is_point_light = dir_length < t_max
        t_max_shadow = dir_length if is_point_light else t_max
        
        shadow_obj, shadow_t = closest_intersection(
            shadow_origin,
            dir_normalized,
            0.0, t_max_shadow,
            objects
        )[:2]
        if shadow_obj is not None:
            continue
        
        intensity = l.calcIntensityAtPoint(
            point,
            normal=normal,
            ray=ray,
            specular=closest_object.specular
        )
        
        if intensity[0] == 0 and intensity[1] == 0 and intensity[2] == 0:
            continue
        
        intensity_r += intensity[0]
        intensity_g += intensity[1]
        intensity_b += intensity[2]

    return (intensity_r, intensity_g, intensity_b)

def trace_ray(O, D, t_min, t_max, objects, lights, background=(255, 255, 255), recursion_depth=2, point=None, normal=None):
    closest_object, closest_t = closest_intersection(O, D, t_min, t_max, objects)

    if closest_object is None:
        return sky.sample(D)
    
    if point is None:
        point = (O[0] + D[0]*closest_t, O[1] + D[1]*closest_t, O[2] + D[2]*closest_t)
    if normal is None:
        normal = closest_object.get_normal(point)
    
    intensity_r, intensity_g, intensity_b = compute_lighting(
        point, normal, D, closest_object, lights, objects, t_max, t_min
    )
    
    c0, c1, c2 = closest_object.color
    final_r = min(255, int(c0 * intensity_r))
    final_g = min(255, int(c1 * intensity_g))
    final_b = min(255, int(c2 * intensity_b))
    
    r = closest_object.reflective
    if recursion_depth <= 0 or r <= 1e-3:
        return (final_r, final_g, final_b)
    
    R = getReflectedRay(D, normal)
    P_offset = add(point, mul(normal, 0.001))
    
    reflected_color = trace_ray(
        P_offset, R, 0.001, t_max, objects, lights, background, recursion_depth - 1
    )
    
    one_minus_r = 1 - r
    return (
        min(255, int(final_r * one_minus_r + reflected_color[0] * r)),
        min(255, int(final_g * one_minus_r + reflected_color[1] * r)),
        min(255, int(final_b * one_minus_r + reflected_color[2] * r))
    )

def getReflectedRay(D, N):
    dot_D_N = dot(D, N)
    return sub(D, mul(N, 2 * dot_D_N))


def render_row(args):
    j, width, camera_get_ray_dir, camera_pos, scene_objects, scene_lights = args
    
    row_pixels = []
    t_max = math.inf
    
    for i in range(width):
        D = camera_get_ray_dir(i, j)
        color = trace_ray(
            camera_pos, D, 
            t_min=1.0, t_max=t_max, 
            objects=scene_objects,
            lights=scene_lights
        )
        row_pixels.append((i, j, color))
    
    return row_pixels


class RaytracerApp:
    
    def __init__(self, scene):
        self.camera = scene.camera
        self.scene = scene

        self.img = Image.new("RGB", (self.camera.Cw, self.camera.Ch), (255, 255, 255))
        self.px = self.img.load()
        
        self.half_w = self.camera.Cw // 2
        self.half_h = self.camera.Ch // 2
        self.scene_objects = self.scene.objects
        self.scene_lights = self.scene.lights
        self.camera_pos = self.camera.pos
        
        self.num_processes = cpu_count()
        self.pool = Pool(processes=self.num_processes)
        print(f"Utilisation de {self.num_processes} coeurs")
        
    def render_animation(self):
        frames = []
    
        for frame in range(self.scene.animation_steps):
            print(f"Rendu de la frame {frame + 1}/{self.scene.animation_steps}...")
        
            self.scene.update_frame(frame)
        
            self.scene_objects = self.scene.objects
        
            self.render()
        
            frames.append(self.img.copy())
    
        save_gif(self, frames)

    def render(self):
        print("Début du rendu...")
        
        # Il faut passer les arguments de cette manière pour le multiprocessing (C'est python faut pas chercher à comprendre)
        row_args = []
        for j in range(self.camera.Ch):
            row_args.append((
                j,
                self.camera.Cw,
                self.camera.get_ray_direction,
                self.camera_pos,
                self.scene_objects,
                self.scene_lights
            ))
        
        results = self.pool.map(render_row, row_args)
        
        for row_pixels in results:
            for i, j, color in row_pixels:
                self.px[i, j] = color
        
        print("Rendu terminé !")

    def save(self):
        """Sauvegarde l'image dans ./out/[date].jpg"""
        os.makedirs("out", exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"out/{timestamp}.jpg"
        
        self.img.save(filename, "JPEG", quality=95)
        print(f"Image sauvegardée: {filename}")
        
        return filename

    def run(self):
        """Lance le rendu et sauvegarde l'image."""
        try:
            self.render()
            self.save()
        finally:
            self.pool.close()
            self.pool.join()

