# Python Raytracer - Structure du projet

## Organisation des fichiers

```
python-raytracer/
│
├── main.py                 # Point d'entrée de l'application
│
├── core/                   # Composants principaux
│   ├── __init__.py
│   ├── camera.py          # Gestion de la caméra
│   ├── scene.py           # Configuration de la scène
│   └── graphics.py        # Moteur de rendu et interface Tkinter
│
├── objects/               # Objets 3D
│   ├── __init__.py
│   ├── AbstractObject.py  # Classe de base pour les objets
│   ├── sphere_utils.py    # Implémentation des sphères
│   └── Plane.py          # Implémentation des plans
│
├── lights/               # Sources de lumière
│   ├── __init__.py
│   ├── AbstractLight.py   # Classe de base pour les lumières
│   ├── AmbientLight.py    # Lumière ambiante
│   ├── DirLight.py        # Lumière directionnelle
│   └── PointLight.py      # Lumière ponctuelle
│
└── utils/                # Utilitaires
    ├── __init__.py
    ├── maths.py           # Fonctions mathématiques (vecteurs, etc.)
    └── lightning_utils.py # Calculs d'éclairage
```

## Utilisation

```bash
python main.py
```
