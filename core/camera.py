from utils.maths import normalize, mul
import math

class Camera:
    
    def __init__(self, canvas_width=600, canvas_height=400):
        self.Cw = canvas_width
        self.Ch = canvas_height

        self.Vw = 5.0
        self.Vh = 3.5
        self.d = 1.0 
        
        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        
        self.pos = (0.0, 0.5, 0.0)
        self.update_dir()
        
        self.vw_cw_ratio = self.Vw / self.Cw
        self.vh_ch_ratio = self.Vh / self.Ch
        
    def update_dir(self):
        # Clamp pitch to avoid gimbal lock
        self.pitch = max(-89.0, min(89.0, self.pitch))
        # Direction vector
        self.dir = (
            math.cos(math.radians(self.pitch)) * math.sin(math.radians(self.yaw)),
            math.sin(math.radians(self.pitch)),
            math.cos(math.radians(self.pitch)) * math.cos(math.radians(self.yaw))
        )
        self.dir = normalize(self.dir)

        # Up vector (global up)
        world_up = (0.0, 1.0, 0.0)
        # Right = dir x world_up
        self.right = normalize((
            self.dir[1]*world_up[2] - self.dir[2]*world_up[1],
            self.dir[2]*world_up[0] - self.dir[0]*world_up[2],
            self.dir[0]*world_up[1] - self.dir[1]*world_up[0]
        ))
        # Up = right x dir
        self.up = normalize((
            self.right[1]*self.dir[2] - self.right[2]*self.dir[1],
            self.right[2]*self.dir[0] - self.right[0]*self.dir[2],
            self.right[0]*self.dir[1] - self.right[1]*self.dir[0]
        ))
        # Roll non géré

    def canvas_to_viewport(self, x, y):
        return (
            x * self.vw_cw_ratio,
            y * self.vh_ch_ratio,
            self.d
        )
    
    def get_ray_direction(self, i, j):
        
        half_w = self.Cw // 2
        half_h = self.Ch // 2
        
        x = i - half_w
        y = half_h - j
        
        D = self.canvas_to_viewport(x, y)
        
        dx = mul(self.right, D[0])
        dy = mul(self.up, D[1]*-1)
        dz = mul(self.dir, D[2])
        
        D_dir = (
            dx[0] + dy[0] + dz[0],
            dx[1] + dy[1] + dz[1],
            dx[2] + dy[2] + dz[2]
        )
        
        return normalize(D_dir)