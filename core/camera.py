class Camera:
    
    def __init__(self, canvas_width, canvas_height):
        self.Cw = canvas_width
        self.Ch = canvas_height

        self.Vw = 5.0
        self.Vh = 3.5
        self.d = 1.0 
        self.pos = (0.0, 0.5, 0.0)
        
        self.vw_cw_ratio = self.Vw / self.Cw
        self.vh_ch_ratio = self.Vh / self.Ch
        
        self.move_speed = 0.5
        
        self._ray_directions_cache = None
        self._precompute_ray_directions()
    
    def _precompute_ray_directions(self):
        """Pré-calcule toutes les directions de rayons normalisées."""
        from utils.maths import normalize
        
        half_w = self.Cw // 2
        half_h = self.Ch // 2
        
        self._ray_directions_cache = []
        for j in range(self.Ch):
            row = []
            y = (half_h - j) * self.vh_ch_ratio
            for i in range(self.Cw):
                x = (i - half_w) * self.vw_cw_ratio
                D = normalize((x, y, self.d))
                row.append(D)
            self._ray_directions_cache.append(row)
    
    def get_ray_direction(self, i, j):
        return self._ray_directions_cache[j][i]

    def canvas_to_viewport(self, x, y):
        return (
            x * self.vw_cw_ratio,
            y * self.vh_ch_ratio,
            self.d
        )
    
    def move(self, dx, dy, dz):
        self.pos = (
            self.pos[0] + dx * self.move_speed,
            self.pos[1] + dy * self.move_speed,
            self.pos[2] + dz * self.move_speed
        )
    
    def move_forward(self):
        self.move(0, 0, 1)
    
    def move_backward(self):
        self.move(0, 0, -1)
    
    def move_left(self):
        self.move(-1, 0, 0)
    
    def move_right(self):
        self.move(1, 0, 0)
    
    def move_up(self):
        self.move(0, 1, 0)
    
    def move_down(self):
        self.move(0, -1, 0)
