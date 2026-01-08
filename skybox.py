import math
from PIL import Image

def gradient_sky(D):
    dx, dy, dz = D
    l = math.sqrt(dx*dx + dy*dy + dz*dz)
    if l == 0:
        return (255, 255, 255)
    dy /= l
    t = max(0.0, min(1.0, (dy + 1.0) * 0.5))
    r = int(30 + (180 - 30) * t)
    g = int(60 + (210 - 60) * t)
    b = int(90 + (255 - 90) * t)
    return (r, g, b)

class Skybox:
    def __init__(self, path):
        self.img = Image.open(path).convert("RGB")
        self.w, self.h = self.img.size
        self.px = self.img.load()

    def sample(self, D):
        dx, dy, dz = D
        l = math.sqrt(dx*dx + dy*dy + dz*dz)
        if l == 0:
            return (0, 0, 0)
        dx /= l; dy /= l; dz /= l

        u = 0.5 + math.atan2(dz, dx) / (2.0 * math.pi)
        v = 0.5 - math.asin(dy) / math.pi

        x = int(u * (self.w - 1)) % self.w
        y = int(v * (self.h - 1))
        y = 0 if y < 0 else (self.h - 1 if y >= self.h else y)

        return self.px[x, y]
