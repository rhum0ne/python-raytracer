from objects.Rectangle import Rectangle

class Cube(Rectangle):
    def __init__(self, point, length, color, specular=-1, reflective=0.0, texture=None):
        super().__init__(point, length, length, length, color, specular, reflective, texture)
