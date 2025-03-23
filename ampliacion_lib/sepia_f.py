from PIL import Image
import numpy as np


def apply_custom_filter(image, custom_filter):
    """
        Aplica un filtro personalizado a la imagen utilizando una matriz de transformación de colores.

    Parámetros:
        image - PIL: Imagen original.
        custom_filter - array: Matriz 3x3 que transforma los valores de los 3 canales (RGB).

    Retorna:
        filtered_img - PIL: Imagen con el filtro aplicado.
    """
    img_array = np.array(image)

    if img_array.shape[-1] == 3:
        filtered_img = img_array @ custom_filter.T
        filtered_img = np.clip(filtered_img, 0, 255)
    else:
        raise ValueError("La imagen debe tener 3 canales (RGB).")

    filtered_img = Image.fromarray(filtered_img.astype('uint8'))

    return filtered_img

