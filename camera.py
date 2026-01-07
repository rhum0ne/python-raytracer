class Camera:
    
    def __init__(self, canvas_width=600, canvas_height=400):
        self.Cw = canvas_width
        self.Ch = canvas_height

        self.Vw = 3.0
        self.Vh = 2.0
        self.d = 1.0 
        self.pos = (0.0, 0.0, 0.0)

    def canvas_to_viewport(self, x, y):
        return (
            x * self.Vw / self.Cw,
            y * self.Vh / self.Ch,
            self.d
        )
