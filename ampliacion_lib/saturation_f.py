import cv2
import numpy as np
import random

def apply_saturation_filter(img, saturation_percent):
    """
        Función que aplica un filtro de saturación a la imagen, ajustando los niveles de saturación en función
        de un porcentaje especificado. Puede aumentar o disminuir la saturación aleatoriamente.

    Parámetros:
        img - array: Imagen original en formato BGR.
        saturation_percent - float: Porcentaje de ajuste de saturación (entre 0 y 100).

    Retorna:
        adjusted_img - array: Imagen resultante con el ajuste de saturación aplicado.
    """

    if len(img.shape) == 2 or img.shape[2] == 1:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    saturation_factor = 1 + (saturation_percent / 100.0)

    if random.choice([True, False]):
        saturation_factor = 1 / saturation_factor

    hsv_img[:, :, 1] = np.clip(hsv_img[:, :, 1] * saturation_factor, 0, 255).astype(np.uint8)

    adjusted_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

    return adjusted_img
