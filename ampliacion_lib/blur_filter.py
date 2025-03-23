import cv2
import numpy as np

def apply_blur_filter(img, blur_sigma):
    """
        Aplica un filtro de desenfoque Gaussiano a una imagen.
        Se utiliza la librería cv2 con el módulo GaussianBlur.

    Parámetros:
        img - array: Imagen a la cual se aplicará el filtro.
        blur_sigma - float: Valor de la desviación estándar del filtro Gaussiano.
                        Cuanto mayor sea el valor, mayor será el desenfoque.

    Retorna:
        blurred_img - array: Imagen aplicada el desenfoque.
    """
    kernel_size = int(blur_sigma * 6) | 1

    blurred_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), blur_sigma)

    return blurred_img


