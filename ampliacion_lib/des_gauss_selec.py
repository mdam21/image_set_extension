import json
import os
import cv2
import numpy as np


def apply_selective_gaussian_blur(img, threshold=50):
    """
        Función que aplica un desenfoque gaussiano selectivo en áreas de bajo contraste. Las áreas de bajo contraste son

    Parámetros:
        img - array: Imagen en formato BGR o escala de grises.
        threshold - int: Umbral de contraste para aplicar el desenfoque. Las áreas con contraste
                     menor que este valor serán desenfocadas.

    Retorna:
        result_img - array: Imagen resultante con desenfoque gaussiano selectivo aplicado.
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = cv2.magnitude(sobel_x, sobel_y)

    normalized_gradient = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX)

    mask = (normalized_gradient < threshold).astype(np.uint8) * 255

    blurred_img = cv2.GaussianBlur(img, (11, 11), 0)

    result_img = np.where(mask[..., np.newaxis] == 255, blurred_img, img)

    return result_img


