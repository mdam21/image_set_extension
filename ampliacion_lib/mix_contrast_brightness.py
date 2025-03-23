import json
import os
import cv2
import numpy as np
import random


def apply_brightness_filter(img, brightness_percent, mode="both"):
    """
    Aplica un filtro para ajustar el brillo de una imagen en función de un porcentaje dado.

    Parámetros:
    img (numpy array): Imagen sobre la cual se ajustará el brillo.
    brightness_percent (float): Porcentaje de ajuste de brillo, entre 1 y 99.
    mode (str): Puede ser "positive" para incrementar el brillo, "negative" para reducirlo o "both"
                para elegir aleatoriamente entre aumentar o reducir el brillo.

    Retorna:
    adjusted_img (numpy array): Imagen con el brillo ajustado.
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


def apply_contrast_filter(img, contrast_percent, mode="both"):
    """
    Aplica un filtro para ajustar el contraste de una imagen en función de un porcentaje dado.

    Parámetros:
    img (numpy array): Imagen sobre la cual se ajustará el contraste.
    contrast_percent (float): Porcentaje de ajuste de contraste, entre 1 y 99.
    mode (str): Puede ser "positive" para incrementar el contraste, "negative" para reducirlo o "both"
                para elegir aleatoriamente entre aumentar o reducir el contraste.

    Retorna:
    adjusted_img (numpy array): Imagen con el contraste ajustado.
    """
    if mode == "positive":
        contrast_factor = 1 + (contrast_percent / 100.0)
    elif mode == "negative":
        contrast_factor = 1 - (contrast_percent / 100.0)
    elif mode == "both":
        if random.choice([True, False]):
            contrast_factor = 1 + (contrast_percent / 100.0)
        else:
            contrast_factor = 1 - (contrast_percent / 100.0)
    else:
        raise ValueError("El modo debe ser 'positive', 'negative' o 'both'.")

    # Aplicar contraste, centrándonos en 128 como valor base
    adjusted_img = np.clip(128 + contrast_factor * (img - 128), 0, 255).astype(np.uint8)

    return adjusted_img

