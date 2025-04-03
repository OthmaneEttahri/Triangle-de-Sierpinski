import math
import numpy as np
import pyvista as pv
from scripts import *
import os

# --- Fonctions de génération du modèle fractal ---



def sierpinski_tetra(vertices, depth):
    """
    À partir d'un tétraèdre défini par 4 sommets (vertices),
    retourne la liste des tétraèdres générés à la profondeur 'depth'.
    """
    if depth == 0:
        return [vertices]
    v0, v1, v2, v3 = vertices
    # Calcul des milieux sur chaque arête
    a = midpoint(v0, v1)
    b = midpoint(v0, v2)
    c = midpoint(v0, v3)
    d = midpoint(v1, v2)
    e = midpoint(v1, v3)
    f = midpoint(v2, v3)
    # Les 4 tétraèdres aux sommets (on ignore le tétraèdre central)
    t0 = [v0, a, b, c]
    t1 = [a, v1, d, e]
    t2 = [b, d, v2, f]
    t3 = [c, e, f, v3]
    tetrahedres = []
    tetrahedres += sierpinski_tetra(t0, depth - 1)
    tetrahedres += sierpinski_tetra(t1, depth - 1)
    tetrahedres += sierpinski_tetra(t2, depth - 1)
    tetrahedres += sierpinski_tetra(t3, depth - 1)
    return tetrahedres

def create_initial_tetrahedron(size=1.0):
    """
    Crée un tétraèdre régulier de côté 'size' avec une géométrie simple.
    Points choisis :
      - v0 = (0, 0, 0)
      - v1 = (size, 0, 0)
      - v2 = (size/2, size*sqrt(3)/2, 0)
      - v3 = (size/2, size*sqrt(3)/6, size*sqrt(6)/3)
    """
    return [
        (0, 0, 0),
        (size, 0, 0),
        (size/2, size * math.sqrt(3)/2, 0),
        (size/2, size * math.sqrt(3)/6, size * math.sqrt(6)/3)
    ]

def tetrahedron_to_faces(tetra):
    """
    Convertit un tétraèdre (4 sommets) en 4 faces (triangles).
    """
    v0, v1, v2, v3 = tetra
    return [
        (v0, v1, v2),
        (v0, v1, v3),
        (v0, v2, v3),
        (v1, v2, v3)
    ]

def collect_mesh_data(tetrahedres):
    """
    À partir d'une liste de tétraèdres, collecte une liste unique de sommets
    et la liste des faces correspondantes (chaque face est un triangle).
    """
    vertices = []
    faces = []
    vertex_dict = {}
    
    def add_vertex(v):
        if v not in vertex_dict:
            vertex_dict[v] = len(vertices)
            vertices.append(v)
        return vertex_dict[v]
    
    for tetra in tetrahedres:
        for face in tetrahedron_to_faces(tetra):
            face_indices = tuple(add_vertex(v) for v in face)
            faces.append(face_indices)
    return vertices, faces

# --- Génération du modèle fractal ---
depth = 3  # Par exemple, depth=3 donnera 4^3 = 64 tétraèdres
initial = create_initial_tetrahedron(size=1.0)
tetrahedres = sierpinski_tetra(initial, depth)
vertices, face_indices = collect_mesh_data(tetrahedres)

# Conversion des faces au format PyVista :
faces_list = []
for face in face_indices:
    faces_list.append(3)  # chaque face est un triangle
    faces_list.extend(face)
faces_np = np.array(faces_list)
vertices_np = np.array(vertices)

# Création du mesh PyVista
mesh = pv.PolyData(vertices_np, faces_np)

# --- Création d'un repère (axes) ---
axes_x = pv.Arrow(start=(0, 0, 0), direction=(1, 0, 0),
                  tip_length=0.1, tip_radius=0.02, shaft_radius=0.005)
axes_y = pv.Arrow(start=(0, 0, 0), direction=(0, 1, 0),
                  tip_length=0.1, tip_radius=0.02, shaft_radius=0.005)
axes_z = pv.Arrow(start=(0, 0, 0), direction=(0, 0, 1),
                  tip_length=0.1, tip_radius=0.02, shaft_radius=0.005)

# --- Création d'une grille dans le plan XY (z = 0) ---
def create_grid(xlim=(-0.5, 1.5), ylim=(-0.5, 1.5), spacing=0.1):
    lines = []
    xs = np.arange(xlim[0], xlim[1] + spacing, spacing)
    ys = np.arange(ylim[0], ylim[1] + spacing, spacing)
    # Lignes horizontales
    for y in ys:
        lines.append(np.array([[xlim[0], y, 0],
                                 [xlim[1], y, 0]]))
    # Lignes verticales
    for x in xs:
        lines.append(np.array([[x, ylim[0], 0],
                                 [x, ylim[1], 0]]))
    grid = pv.PolyData()
    for line in lines:
        grid_line = pv.Line(line[0], line[1])
        grid = grid.merge(grid_line)
    return grid

grid = create_grid(xlim=(-0.5, 1.5), ylim=(-0.5, 1.5), spacing=0.1)

# --- Affichage avec PyVista ---
p = pv.Plotter()
p.add_mesh(mesh, color="lightblue", opacity=1, show_edges=True)
p.add_mesh(axes_x, color="red", label="Axe X", reset_camera=False)
p.add_mesh(axes_y, color="green", label="Axe Y", reset_camera=False)
p.add_mesh(axes_z, color="blue", label="Axe Z", reset_camera=False)
p.add_mesh(grid, style="wireframe", color="gray", opacity=0.5)

p.show_axes()  # Affiche un repère dans la scène

p.add_title("Modèle 3D du tétraèdre de Sierpinski", font_size=14)
legend_text = "Légende:\nAxe X : Rouge\nAxe Y : Vert\nAxe Z : Bleu"
p.add_text(legend_text, position="upper_left", font_size=10, color="black")

# Pour rendre le repère horizontal, on définit la vue en XY (la caméra regarde du haut)
p.view_xz()

p.show()
