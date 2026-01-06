from abc import ABC, abstractmethod


class AbstractObject(ABC):
    
    def __init__(self, color):
        self.color = color  # (r, g, b)
    
    @abstractmethod
    def intersect(self, origin, direction):
        """
        Calcule l'intersection entre un rayon et l'objet.
        
        Args:
            origin: Point d'origine du rayon (x, y, z)
            direction: Direction du rayon (x, y, z)
            
        Returns:
            Distance t de l'intersection (math.inf si pas d'intersection)
        """
        return NotImplementedError("intersect must be implemented in subclasses")
    
    @abstractmethod
    def get_normal(self, point):
        """
        Calcule la normale à la surface au point donné.
        
        Args:
            point: Point sur la surface (x, y, z)
            
        Returns:
            Vecteur normal (x, y, z)
        """
        return NotImplementedError("get_normal must be implemented in subclasses")
