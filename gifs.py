from PIL import Image
import os
from datetime import datetime

def save_gif(self, frames):
    os.makedirs("out", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"out/{timestamp}_animation.gif"
    
    # Sauvegarder le GIF
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=100,  # ms par frame (100ms = 10 FPS)
        loop=0  # 0 = boucle infinie
    )
    
    print(f"Animation sauvegardée: {filename}")
    return filename