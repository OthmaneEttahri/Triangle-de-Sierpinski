def midpoint(v1, v2):
    """Retourne le point milieu entre deux points 3D."""
    return tuple((v1[i] + v2[i]) / 2 for i in range(3))