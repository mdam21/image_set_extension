import cv2
import numpy as np
import random


def apply_exposure_filter(img, exposure_percent):
    """
        Función que aplica un filtro de exposición a una imagen, haciendo que sea más brillante o más oscura.

    Parámetros:
        img - array: Imagen sobre la cual se aplicará el filtro.
        exposure_percent - float: Porcentaje de ajuste de exposición, entre 0 y 100.

    Retorna:
        adjusted_img - array: Imagen con la exposición ajustada.
    """
    gamma_min = 0.01
    gamma_max = 100

    if exposure_percent == 0:
        gamma = 1.0
    else:
        if random.choice([True, False]):
            gamma = 1 + (exposure_percent / 100.0) * (gamma_max - 1)
        else:
            gamma = 1 - (exposure_percent / 100.0) * (1 - gamma_min)

    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(0, 256)]).astype("uint8")

    adjusted_img = cv2.LUT(img, table)

    return adjusted_img


