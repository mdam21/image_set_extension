import cv2
import numpy as np


def apply_sobel_filter(img):
    """
        Aplica el filtro Sobel para detectar bordes en la imagen.

    Parámetros:
        img - array: Imagen en formato BGR o escala de grises.

    Retorna:
        sobel_combined - array: Imagen resultante con la magnitud del gradiente aplicada para la detección de bordes.
    """
    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)

    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    sobel_combined = cv2.magnitude(sobel_x, sobel_y)

    sobel_combined = np.clip(sobel_combined, 0, 255).astype(np.uint8)

    return sobel_combined


