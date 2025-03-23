import random


def apply_cutout_filter(img, cutout_percent, num_squares):
    """
        Realiza recuadros de pixeles negros de un tamaño aleatorio y se aplica como una máscara, con el objetivo de eliminar ciertas partes del objeto.

    Parámetros:
        img - array: Imagen a aplicar la máscara.
        cutout_percent - float: Porcentaje del tamaño máximo de recuadro, calculado en relación al tamaño de la imagen.
        num_squares - int: Número de cuadrados que se aplican en la máscara de manera aleatoria..

    Retorna:
        img - array: Imagen con cuadrados de pixeles en negro.
    """
    height, width, _ = img.shape
    square_size = int(cutout_percent / 100.0 * min(height, width))

    for _ in range(num_squares):
        top_left_x = random.randint(0, width - square_size)
        top_left_y = random.randint(0, height - square_size)

        img[top_left_y:top_left_y + square_size, top_left_x:top_left_x + square_size] = 0

    return img


