from abc import ABC, abstractmethod

class AbstractAnimation(ABC):
    @abstractmethod
    def update_frame(self, step):
        """
        Génère la scène à un instant donné t.
        
        Args:
            t: Temps ou frame index
            
        Returns:
            Scène à l'instant t
        """
        return NotImplementedError("get_frame must be implemented in subclasses")