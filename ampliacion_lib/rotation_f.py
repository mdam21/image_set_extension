import json
import os
import numpy as np
import cv2


def rotate_image(img, angle):
    """
        Rota la imagen en el ángulo especificado.

    Parámetros:
        img - array: Imagen original.
        angle - int: Ángulo de rotación (puede ser 90, -90 o 180 grados).

    Retorna:
        numpy: Imagen rotada en el ángulo especificado.
    """
    if angle == 90:
        return np.rot90(img, k=3)  # Rota 270 grados en sentido antihorario (equivalente a 90 en sentido horario)
    elif angle == -90:
        return np.rot90(img, k=1)  # Rota 90 grados en sentido antihorario
    elif angle == 180:
        return np.rot90(img, k=2)  # Rota 180 grados
    return img

