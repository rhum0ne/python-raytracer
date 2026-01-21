from animations.AbstractAnimation import AbstractAnimation

class SphereScaling(AbstractAnimation):
    def __init__(self, scene, sphere, target_size, total_steps=60):
        self.sphere = sphere
        self.initial_radius = sphere.radius
        self.target_size = target_size
        self.total_steps = total_steps
        self.scene = scene
        
    def update_frame(self, step):
        if step >= self.total_steps:
            return
        
        scale_factor = 1 + (self.target_size - self.initial_radius) * (step / self.total_steps)
        self.sphere.radius = self.initial_radius * scale_factor