import numpy as np
import pyvista as pv
from scripts import *

# Fonction récursive pour générer les triangles de Sierpiński
def sierpinski_triangle(vertices, depth):
    if depth == 0:
        return [vertices]
    v0, v1, v2 = vertices
    m0 = midpoint(v0, v1)
    m1 = midpoint(v1, v2)
    m2 = midpoint(v2, v0)
    return (sierpinski_triangle([v0, m0, m2], depth - 1) +
            sierpinski_triangle([m0, v1, m1], depth - 1) +
            sierpinski_triangle([m2, m1, v2], depth - 1))

# Fonction pour créer les maillages 3D avec une épaisseur donnée
def generate_mesh(depth, thickness=0.1):
    base_triangle = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0.5, np.sqrt(3)/2, 0]
    ])
    triangles = sierpinski_triangle(base_triangle, depth)
    meshes = []
    for tri in triangles:
        faces = np.hstack([[3, 0, 1, 2]])
        poly = pv.PolyData(tri, faces)
        extruded = poly.extrude([0, 0, thickness], capping=True)
        meshes.append(extruded)
    return meshes

# Définir le niveau de profondeur et l'épaisseur
depth = 2
thickness = 0.05

# Générer les maillages
meshes = generate_mesh(depth, thickness)

# Créer un plotter PyVista
plotter = pv.Plotter()

# Ajouter chaque maillage au plotter avec des couleur et des libellé
for i, mesh in enumerate(meshes):
    color = 'red' 
    label = 'Triangle'
    plotter.add_mesh(mesh, color=color, show_edges=False, opacity=1.0, label=label)

# Ajouter le repère au centre
plotter.add_axes_at_origin()

# Afficher la grille avec des étiquettes personnalisées
plotter.show_grid()

# Ajouter la légende
#plotter.add_legend()

# Afficher le rendu
plotter.show()




