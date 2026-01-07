from abc import ABC, abstractmethod


class AbstractLight(ABC):
    
    def __init__(self, intensity):
        self.intensity = intensity  # (r, g, b)
    
    @abstractmethod
    def calcIntensityAtPoint(self, point, normal, ray, specular=-1):
        """
        Calcule l'intensité de la lumière à un point donné.
        
        Args:
            point: Position du point (x, y, z)
            normal: Vecteur normal au point (x, y, z)
            
        Returns:
            Tuple (r, g, b) représentant l'intensité de la lumière
        """
        return NotImplementedError("calcIntensityAtPoint must be implemented in subclasses")

    @abstractmethod
    def get_direction_from_point(self, point):
        """
        Calcule la direction de la lumière depuis un point donné.
        
        Args:
            point: Position du point (x, y, z)
            
        Returns:
            Vecteur directionnel (x, y, z) ou None si la lumière n'a pas de direction (Ambiante)
        """
        return NotImplementedError("get_direction_from_point must be implemented in subclasses")