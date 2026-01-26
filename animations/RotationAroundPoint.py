from animations.AbstractAnimation import AbstractAnimation
import numpy as np

class RotationAroundPoint(AbstractAnimation):
    
    
    def __init__(self, scene, object, axis, angle, total_steps=60, point_central=(0,0,0)):
        self.object = object
        self.axis = axis
        self.angle = angle
        self.total_steps = total_steps
        self.scene = scene
        self.point_central = np.array(point_central)
        self.rotation_matrix = self._create_rotation_matrix(axis)
        
    def update_frame(self, step):
        pos = self.object.get_position()
        num_pos = np.array([pos[0], pos[1], pos[2]])
        # Translation pour centrer autour du point_central
        relative_pos = num_pos - self.point_central
        rotated_relative =  relative_pos @ self.rotation_matrix
        rotated_pos = rotated_relative + self.point_central
        self.object.set_positions((rotated_pos[0], rotated_pos[1], rotated_pos[2]))
    
    def _create_rotation_matrix(self, axis):
        ux, uy, uz = axis
        
        cos_a = np.cos(self.angle)
        sin_a = np.sin(self.angle)
        
        rotation_matrix = np.array([
            [cos_a + ux*ux*(1 - cos_a),      ux*uy*(1 - cos_a) - uz*sin_a, ux*uz*(1 - cos_a) + uy*sin_a],
            [uy*ux*(1 - cos_a) + uz*sin_a,   cos_a + uy*uy*(1 - cos_a),    uy*uz*(1 - cos_a) - ux*sin_a],
            [uz*ux*(1 - cos_a) - uy*sin_a,   uz*uy*(1 - cos_a) + ux*sin_a, cos_a + uz*uz*(1 - cos_a)]
        ])
        
        return rotation_matrix