class Camera:
    
    def __init__(self, canvas_width=600, canvas_height=400):
        self.Cw = canvas_width
        self.Ch = canvas_height

        self.Vw = 5.0
        self.Vh = 3.5
        self.d = 1.0 
        self.pos = (0.0, 0.5, 0.0)
        
        self.vw_cw_ratio = self.Vw / self.Cw
        self.vh_ch_ratio = self.Vh / self.Ch

    def canvas_to_viewport(self, x, y):
        return (
            x * self.vw_cw_ratio,
            y * self.vh_ch_ratio,
            self.d
        )
