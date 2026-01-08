from animations.AbstractAnimation import AbstractAnimation

class LinearMove(AbstractAnimation):
    def __init__(self, scene, object, target_position, total_steps=60):
        self.object = object
        self.initial_position = object.get_position()
        self.target_position = target_position
        self.total_steps = total_steps
        self.scene = scene
        
    def update_frame(self, step):
        if step >= self.total_steps:
            return
        
        new_x = self.initial_position[0] + (self.target_position[0] - self.initial_position[0]) * (step / self.total_steps)
        new_y = self.initial_position[1] + (self.target_position[1] - self.initial_position[1]) * (step / self.total_steps)
        new_z = self.initial_position[2] + (self.target_position[2] - self.initial_position[2]) * (step / self.total_steps)
        
        self.object.center = (new_x, new_y, new_z)