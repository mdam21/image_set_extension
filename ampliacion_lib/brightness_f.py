import numpy as np
import random


def apply_brightness_filter(img, brightness_percent, mode="both"):
    """
        Modifica el brillo de una imagen en función de un porcentaje dado, ocupamos numpy para modificar el valor
        de la matriz de la imagen.

    Parámetros:
        img - array: Imagen a la que se ajustará el brillo.
        brightness_percent - float: Porcentaje de ajuste de brillo entre 1-99.
        mode - str: Modo de incremento, decremento o ambos, positive negative both respectivamente.

    Retorna:
        adjusted_img - array: Imagen con el brillo ajustado.
    """

    if mode == "positive":
        brightness_factor = 1 + (brightness_percent / 100.0)
    elif mode == "negative":
        brightness_factor = 1 - (brightness_percent / 100.0)
    elif mode == "both":
        if random.choice([True, False]):
            brightness_factor = 1 + (brightness_percent / 100.0)
        else:
            brightness_factor = 1 - (brightness_percent / 100.0)
    else:
        raise ValueError("El modo debe ser 'positive', 'negative' o 'both'.")

    adjusted_img = np.clip(img * brightness_factor, 0, 255).astype(np.uint8)

    return adjusted_img


