from core.graphics import RaytracerApp
from core.scene import Scene


if __name__ == "__main__":
    scene = Scene()
    scene.loadScene("tutorial_scene.json")
    app = RaytracerApp(scene=scene)
    if scene.animation_steps == 1:
        app.run()
    
    else:
        app.render_animation()
