import json
import os
import cv2
import numpy as np
import random


def apply_saturation_filter(img, saturation_percent):
    """
    Aplica un filtro de saturación a la imagen, ajustando los niveles de saturación en función
    de un porcentaje especificado. Puede aumentar o disminuir la saturación aleatoriamente.

    Parámetros:
    img (numpy array): Imagen original en formato BGR.
    saturation_percent (float): Porcentaje de ajuste de saturación (entre 0 y 100).

    Retorna:
    adjusted_img (numpy array): Imagen resultante con el ajuste de saturación aplicado.
    """
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Calcular el factor de saturación (1 + porcentaje/100.0) para aumentar la saturación
    saturation_factor = 1 + (saturation_percent / 100.0)
    if random.choice([True, False]):
        saturation_factor = 1 / saturation_factor  # Aleatoriamente reducir la saturación

    # Ajustar el canal de saturación (canal 1 en HSV), manteniendo el rango [0, 255]
    hsv_img[:, :, 1] = np.clip(hsv_img[:, :, 1] * saturation_factor, 0, 255).astype(np.uint8)

    # Convertir de vuelta de HSV a BGR para obtener la imagen final
    adjusted_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

    return adjusted_img


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
        brightness_factor = 1 + (brightness_percent / 100.0)  # Aumenta el brillo
    elif mode == "negative":
        brightness_factor = 1 - (brightness_percent / 100.0)  # Disminuye el brillo
    elif mode == "both":
        if random.choice([True, False]):
            brightness_factor = 1 + (brightness_percent / 100.0)  # Aumenta el brillo
        else:
            brightness_factor = 1 - (brightness_percent / 100.0)  # Disminuye el brillo
    else:
        raise ValueError("El modo debe ser 'positive', 'negative' o 'both'.")

    # Aplicar el ajuste de brillo
    adjusted_img = np.clip(img * brightness_factor, 0, 255).astype(np.uint8)

    return adjusted_img


def apply_combined_filter(img, saturation_percent, brightness_percent, brightness_mode="both"):
    """
    Aplica un filtro combinado de ajuste de saturación y brillo a la imagen.

    Parámetros:
    img (numpy array): Imagen original en formato BGR.
    saturation_percent (float): Porcentaje de ajuste de saturación (entre 0 y 100).
    brightness_percent (float): Porcentaje de ajuste de brillo (entre 1 y 99).
    brightness_mode (str): Modo de ajuste del brillo ("positive", "negative" o "both").

    Retorna:
    img_combined (numpy array): Imagen con los ajustes de saturación y brillo aplicados.
    """
    # Aplicar el filtro de saturación
    img_saturation = apply_saturation_filter(img, saturation_percent)

    # Aplicar el filtro de brillo sobre la imagen ya ajustada en saturación
    img_combined = apply_brightness_filter(img_saturation, brightness_percent, brightness_mode)

    return img_combined

