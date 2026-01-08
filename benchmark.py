import time
import math
from core.camera import Camera
from core.scene import Scene
from utils.maths import normalize
from core.graphics import trace_ray

def benchmark_rendering(num_samples=1000):
    camera = Camera(canvas_width=800, canvas_height=600)
    scene = Scene()
    
    half_w = camera.Cw // 2
    half_h = camera.Ch // 2
    
    print("🚀 Benchmark du raytracer avec Numba JIT")
    print(f"Échantillons: {num_samples} pixels")
    print("-" * 50)
    
    print("Warm-up du JIT compiler...")
    for i in range(100):
        x = (i % 20 - 10) * camera.vw_cw_ratio
        y = (i // 20 - 5) * camera.vh_ch_ratio
        D = normalize((x, y, camera.d))
        trace_ray(camera.pos, D, 1.0, math.inf, scene.objects, scene.lights)
    
    print("JIT compilé, début du benchmark...")
    
    # Benchmark réel
    start_time = time.perf_counter()
    
    for i in range(num_samples):
        x = ((i % 100) - 50) * camera.vw_cw_ratio
        y = ((i // 100) - 5) * camera.vh_ch_ratio
        D = normalize((x, y, camera.d))
        trace_ray(camera.pos, D, 1.0, math.inf, scene.objects, scene.lights)
    
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    
    print(f"\n✅ Temps total: {elapsed:.3f} secondes")
    print(f"⚡ Pixels/seconde: {num_samples / elapsed:.0f}")
    print(f"📊 Temps moyen par pixel: {elapsed * 1000 / num_samples:.3f} ms")
    
    # Estimation pour une image complète
    total_pixels = camera.Cw * camera.Ch
    estimated_time = (total_pixels / num_samples) * elapsed
    print(f"\n🖼️  Estimation pour {camera.Cw}x{camera.Ch} ({total_pixels:,} pixels):")
    print(f"   Temps estimé: {estimated_time:.1f} secondes ({estimated_time/60:.1f} minutes)")

if __name__ == "__main__":
    benchmark_rendering(5000)
