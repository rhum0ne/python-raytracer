import math
import tkinter as tk
from multiprocessing import Pool, cpu_count
from numba import jit

from PIL import Image, ImageTk
from core.camera import Camera
from core.scene import Scene
from utils.maths import mul, sub, dot, normalize, add, length
from skybox import Skybox
from skybox import gradient_sky

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

@jit(nopython=True, cache=True, fastmath=True)
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
    
    def __init__(self):
        self.camera = Camera(canvas_width=1200, canvas_height=800)
        self.scene = Scene()

        self.root = tk.Tk()
        self.root.title("Python Raytracing")
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)

        self.img = Image.new("RGB", (self.camera.Cw, self.camera.Ch), (255, 255, 255))
        self.px = self.img.load()

        self.tk_img = None
        self.label = tk.Label(self.root)
        self.label.pack(expand=True, fill="both")

        self.playing = True
        self.current_row = 0
        self.rows_per_tick = 800
        
        self.half_w = self.camera.Cw // 2
        self.half_h = self.camera.Ch // 2
        self.scene_objects = self.scene.objects
        self.scene_lights = self.scene.lights
        self.camera_pos = self.camera.pos
        
        self.num_processes = cpu_count()
        self.pool = Pool(processes=self.num_processes)
        
        self.root.bind('<KeyPress>', self.on_key_press)

        self.update_tk_image()
        self.root.after(0, self.render_tick)

    def update_tk_image(self):
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.label.configure(image=self.tk_img)

    def render_tick(self):
        if not self.playing:
            return

        y0 = self.current_row
        y1 = min(self.camera.Ch, y0 + self.rows_per_tick)

        # Préparer les arguments pour chaque ligne
        row_args = []
        for j in range(y0, y1):
            row_args.append((
                j,
                self.camera.Cw,
                self.camera.get_ray_direction,
                self.camera_pos,
                self.scene_objects,
                self.scene_lights
            ))
        
        # Rendre les lignes en parallèle
        results = self.pool.map(render_row, row_args)
        
        # Appliquer les pixels à l'image
        for row_pixels in results:
            for i, j, color in row_pixels:
                self.px[i, j] = color

        self.current_row = y1
        self.update_tk_image()

        if self.current_row < self.camera.Ch:
            self.root.after(1, self.render_tick)

    def restart(self):
        """Recommence le rendu depuis le début."""
        self.img.paste((255, 255, 255), (0, 0, self.camera.Cw, self.camera.Ch))
        self.current_row = 0
        self.camera_pos = self.camera.pos
        self.update_tk_image()
        self.root.after(0, self.render_tick)
    
    def on_key_press(self, event):
        moved = False
        
        # WASD ou flèches pour les déplacements
        if event.keysym in ('w', 'W', 'Up'):
            self.camera.move_forward()
            moved = True
        elif event.keysym in ('s', 'S', 'Down'):
            self.camera.move_backward()
            moved = True
        elif event.keysym in ('a', 'A', 'Left'):
            self.camera.move_left()
            moved = True
        elif event.keysym in ('d', 'D', 'Right'):
            self.camera.move_right()
            moved = True
        elif event.keysym in ('q', 'Q'):
            self.camera.move_down()
            moved = True
        elif event.keysym in ('e', 'E'):
            self.camera.move_up()
            moved = True
        elif event.keysym == 'r':
            self.restart()
            return
        
        if moved:
            self.restart()

    def shutdown(self):
        self.playing = False
        self.pool.close()
        self.pool.join()
        self.root.destroy()

    def run(self):
        self.root.mainloop()