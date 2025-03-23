import json
import os
import numpy as np
import cv2


def crop_image(img, box, crop_percent):
    """
        Recorta una imagen en torno a una caja delimitadora, añadiendo un porcentaje de margen.

    Parámetros:
        img - array: Imagen que se va a recortar.
        box - tuple: Coordenadas de la caja (x, y, ancho, alto) alrededor de la cual se recortará la imagen.
        crop_percent - float: Porcentaje de margen adicional para incluir alrededor de la caja.

    Retorna:
        cropped_img - array: Imagen recortada.
        (start_x, start_y) - tupla: Coordenadas de la esquina superior izquierda del recorte.
    """
    x, y, width, height = map(int, box)
    crop_amount_w = int(width * crop_percent)
    crop_amount_h = int(height * crop_percent)

    start_x = max(0, int(x - crop_amount_w))
    end_x = min(img.shape[1], int(x + width + crop_amount_w))

    start_y = max(0, int(y - crop_amount_h))
    end_y = min(img.shape[0], int(y + height + crop_amount_h))

    cropped_img = img[start_y:end_y, start_x:end_x]
    return cropped_img, (start_x, start_y)

