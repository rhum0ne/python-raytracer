from core.graphics import RaytracerApp
from core.scene import Scene


if __name__ == "__main__":
    scene = Scene()
    
    app = RaytracerApp(scene=scene)
    app.run()
