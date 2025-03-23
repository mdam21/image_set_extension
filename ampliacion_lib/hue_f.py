import json
import os
import cv2
import numpy as np
import random


def apply_hue_filter(img, max_hue_shift_degrees):
    """
        Aplica un filtro de ajuste de hue (tono) a una imagen, realizando un desplazamiento aleatorio
        del hue dentro del rango especificado.

    Parámetros:
        img - array: Imagen original en formato BGR.
        max_hue_shift_degrees - int: Máximo desplazamiento aleatorio del hue en grados (entre 0 y 179).

    Retorna:
        adjusted_img - array: Imagen resultante con el ajuste de hue aplicado.
    """
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue_shift = random.randint(0, max_hue_shift_degrees)
    hue_shift = hue_shift if random.choice([True, False]) else -hue_shift

    hsv_img[:, :, 0] = (hsv_img[:, :, 0].astype(int) + hue_shift) % 180

    adjusted_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

    return adjusted_img

