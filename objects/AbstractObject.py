from abc import ABC, abstractmethod


class AbstractObject(ABC):
    
    def __init__(self, color, specular=10.0, reflective=0.0):
        self.color = color  # (r, g, b)
        self.specular = specular
        self.reflective = reflective
    
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
    
    @abstractmethod
    def get_position(self):
        """
        Retourne la position de l'objet dans l'espace.
        Doit être implémenté dans les sous-classes si applicable.
        
        Returns:
            Position de l'objet (x, y, z)
        """
        raise NotImplementedError("get_position must be implemented in subclasses if applicable")

    @abstractmethod
    def get_size(self):
        """Return the size of the current object. The radius if it's a sphere, the length if it's a cube, and none if it's a plane.
        """
        raise NotImplementedError("get_size must be implemented in subclasses")