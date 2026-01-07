import math
import tkinter as tk

try:
    from PIL import Image, ImageTk
except ImportError:
    raise SystemExit("Pillow manquant. Installe-le avec: pip install pillow")
from core.camera import Camera
from core.scene import Scene
from utils.maths import mul, sub, dot, normalize, add, length

def closest_intersection(O, D, t_min, t_max, objects):
    closest_t = math.inf
    closest_color = None
    closest_object = None

    for obj in objects:
        intersection = obj.intersect(O, D)

        if t_min <= intersection < closest_t:
            if intersection > t_max:
                continue
            closest_t = intersection
            closest_color = obj.color
            closest_object = obj
            
            if closest_t < t_min * 1.01:
                break

    return closest_object, closest_t, closest_color

def compute_lighting_optimized(point, normal, ray, closest_object, lights, objects, t_max, t_min=0.001):
    intensity_r = 0.0
    intensity_g = 0.0
    intensity_b = 0.0
    
    shadow_origin = add(point, mul(normal, 0.001))
    
    for l in lights:
        dir = l.get_direction_from_point(point)
        if dir is None:
            continue
        
        dir_length = length(dir)
        if dir_length < 1e-10:
            continue
        
        dir_normalized = normalize(dir)
            
        t_max_shadow = dir_length if hasattr(l, 'position') else t_max
        
        shadow_obj, shadow_t, _ = closest_intersection(
            shadow_origin,
            dir_normalized,
            0.0, t_max_shadow,
            objects
        )
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
    closest_object, closest_t, closest_color = closest_intersection(O, D, t_min, t_max, objects)

    if closest_color is None:
        return background
    
    if point is None:
        point = (O[0] + D[0]*closest_t, O[1] + D[1]*closest_t, O[2] + D[2]*closest_t)
    if normal is None:
        normal = closest_object.get_normal(point)
    
    intensity_r, intensity_g, intensity_b = compute_lighting_optimized(
        point, normal, D, closest_object, lights, objects, t_max, t_min
    )
        
    closest_color = (
            min(255, int(closest_color[0] * intensity_r)),
            min(255, int(closest_color[1] * intensity_g)),
            min(255, int(closest_color[2] * intensity_b))
        )
    
    r = closest_object.reflective
    if recursion_depth <= 0 or r <= 1e-3:
        return closest_color
    
    R = getReflectedRay(D, normal)
    P_offset = add(point, mul(normal, 0.001))
    
    reflected_color = trace_ray(
        P_offset, R, 0.001, t_max, objects, lights, background, recursion_depth - 1
    )

    return (
        int(closest_color[0] * (1 - r) + reflected_color[0] * r),
        int(closest_color[1] * (1 - r) + reflected_color[1] * r),
        int(closest_color[2] * (1 - r) + reflected_color[2] * r)
    )

def getReflectedRay(D, N):
    dot_D_N = dot(D, N)
    return sub(D, mul(N, 2 * dot_D_N))


class RaytracerApp:
    """Application principale de raytracing avec interface Tkinter."""
    
    def __init__(self):
        # Créer la caméra et la scène
        self.camera = Camera(canvas_width=1200, canvas_height=800)
        self.scene = Scene()

        # Tk window
        self.root = tk.Tk()
        self.root.title("Python Raytracing")
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)

        # Image buffer (Pillow)
        self.img = Image.new("RGB", (self.camera.Cw, self.camera.Ch), (255, 255, 255))
        self.px = self.img.load()

        self.tk_img = None
        self.label = tk.Label(self.root)
        self.label.pack(expand=True, fill="both")

        # Render state
        self.playing = True
        self.current_row = 0
        self.rows_per_tick = 30  # augmente pour accélérer

        self.update_tk_image()
        self.root.after(0, self.render_tick)

    def update_tk_image(self):
        """Convertir l'image Pillow -> Tkinter."""
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.label.configure(image=self.tk_img)

    def render_tick(self):
        """Effectue une partie du rendu à chaque tick."""
        if not self.playing:
            return

        y0 = self.current_row
        y1 = min(self.camera.Ch, y0 + self.rows_per_tick)

        half_w = self.camera.Cw // 2
        half_h = self.camera.Ch // 2

        for j in range(y0, y1):
            # conversion pixel->coord centrée (y inversé pour "haut" positif)
            y = (half_h - j)
            for i in range(self.camera.Cw):
                x = (i - half_w)

                D = self.camera.canvas_to_viewport(x, y)
                # Normaliser la direction pour avoir des distances cohérentes
                D = normalize(D)
                color = trace_ray(
                    self.camera.pos, D, 
                    t_min=1.0, t_max=math.inf, 
                    objects=self.scene.objects,
                    lights=self.scene.lights
                )
                self.px[i, j] = color

        self.current_row = y1

        # rafraîchit l'image de temps en temps
        self.update_tk_image()

        if self.current_row < self.camera.Ch:
            self.root.after(1, self.render_tick)  # 1ms => UI reste fluide

    def restart(self):
        """Recommence le rendu depuis le début."""
        self.img.paste((255, 255, 255), (0, 0, self.camera.Cw, self.camera.Ch))
        self.current_row = 0
        self.update_tk_image()
        self.root.after(0, self.render_tick)

    def shutdown(self):
        """Arrête proprement l'application."""
        self.playing = False
        self.root.destroy()

    def run(self):
        """Lance la boucle principale."""
        self.root.mainloop()

