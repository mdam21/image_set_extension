import json
import os
import numpy as np
from PIL import Image, ImageFilter


def apply_blur_filter(img, blur_radius):
    """
    Aplica un filtro de desenfoque Gaussiano a la imagen.

    Parámetros:
    img (PIL Image): Imagen original.
    blur_radius (float): Radio del desenfoque Gaussiano.

    Retorna:
    blurred_img (PIL Image): Imagen desenfocada con el radio especificado.
    """
    # Aplicar el filtro de desenfoque (GaussianBlur)
    blurred_img = img.filter(ImageFilter.GaussianBlur(blur_radius))
    return blurred_img


def apply_grayscale_filter(img, grayscale_percent):
    """
    Aplica un filtro de escala de grises parcial a una imagen, mezclando la imagen original
    con una versión en escala de grises en función de un porcentaje especificado.

    Parámetros:
    img (PIL Image): Imagen original en formato RGB.
    grayscale_percent (int): Porcentaje de escala de grises a aplicar (0 a 100).

    Retorna:
    blended_img (PIL Image): Imagen resultante con el ajuste de escala de grises aplicado.
    """
    if grayscale_percent < 0 or grayscale_percent > 100:
        raise ValueError("El porcentaje de escala de grises debe estar entre 0 y 100.")

    # Convertir la imagen a escala de grises
    gray_img = img.convert("L").convert("RGB")  # Convertir a "L" (escala de grises) y luego a "RGB"

    # Convertir las imágenes a arrays NumPy para poder mezclarlas
    img_array = np.array(img)
    gray_img_array = np.array(gray_img)

    # Mezclar las imágenes utilizando el porcentaje especificado
    blended_img_array = np.uint8(
        img_array * (1 - grayscale_percent / 100.0) + gray_img_array * (grayscale_percent / 100.0))

    # Convertir de nuevo a imagen PIL
    blended_img = Image.fromarray(blended_img_array)

    return blended_img

