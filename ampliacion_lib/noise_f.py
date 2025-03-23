import numpy as np
from skimage.util import random_noise


def apply_noise_filter(img, noise_amount):
    """
        Aplica un filtro de ruido a la imagen.

    Parámetros:
        img - array: Imagen original en formato BGR.
        noise_amount - float: Cantidad de ruido a aplicar (entre 0 y 1), donde 0 significa sin ruido
                          y 1 significa máximo ruido.

    Retorna:
        noisy_img - array: Imagen con ruido aplicado.
    """
    noisy_img = random_noise(img, mode='s&p', amount=noise_amount)

    noisy_img = np.array(255 * noisy_img, dtype=np.uint8)

    return noisy_img


