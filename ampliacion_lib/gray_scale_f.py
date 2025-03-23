
import cv2


def first_apply_grayscale_filter(img, grayscale_percent):
    """
        Aplica un filtro de escala de grises a una imagen en función a un porcentaje especificado.

    Parámetros:
        img - array: Imagen en color original.
        grayscale_percent - int: Porcentaje de conversión a escala de grises (0 = sin cambio, 100 = completamente en grises).

    Retorna:
        blended_img - array: Imagen resultante mezclada entre la versión en color y la de escala de grises.
    """
    if grayscale_percent < 0 or grayscale_percent > 100:
        raise ValueError("El porcentaje de escala de grises debe estar entre 0 y 100.")

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)

    blended_img = cv2.addWeighted(img, 1 - grayscale_percent / 100.0, gray_img, grayscale_percent / 100.0, 0)

    return blended_img

