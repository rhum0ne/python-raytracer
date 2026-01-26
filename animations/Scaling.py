from objects.AbstractObject import AbstractObject
from animations.AbstractAnimation import AbstractAnimation

class Scaling(AbstractAnimation):
    def __init__(self, scene, object: AbstractObject, target_size, total_steps=60):
        self.object = object
        self.total_steps = total_steps
        self.scene = scene
        self.target_size = target_size
        self.size = object.get_size()
    
    def update_frame(self, step):
        if step >= self.total_steps:
            return
        
        scale_factor = 1 + (self.target_size - self.size) * (step / self.total_steps)
        self.object.radius = self.size * scale_factor