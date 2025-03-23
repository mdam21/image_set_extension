import numpy as np
from scipy.ndimage import map_coordinates, gaussian_filter

def elastic_transform(image, alpha, sigma, random_state=None):
    """
        Función que aplica una transformación elástica a una imagen.

    Parámetros:
        image - array: Imagen a la cual se le aplicará la transformación.
        alpha - float: Factor de escala que controla la intensidad de la deformación.
        sigma - float: Desviación estándar del filtro gaussiano que suaviza la deformación.
        random_state - RandomState: Estado aleatorio para la generación de desplazamientos. Si es None, se genera uno nuevo.

    Retorna:
        distorted_image - array: Imagen distorsionada tras aplicar la transformación elástica.
    """
    if random_state is None:
        random_state = np.random.RandomState(None)

    shape = image.shape
    shape_size = shape[:2]

    dx = gaussian_filter((random_state.rand(*shape_size) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dy = gaussian_filter((random_state.rand(*shape_size) * 2 - 1), sigma, mode="constant", cval=0) * alpha

    x, y = np.meshgrid(np.arange(shape_size[1]), np.arange(shape_size[0]))
    indices = np.reshape(y + dy, (-1, 1)), np.reshape(x + dx, (-1, 1))

    distorted_image = np.zeros_like(image)
    for i in range(shape[2]):  # Para cada canal (ej. R, G, B)
        distorted_image[..., i] = map_coordinates(image[..., i], indices, order=1, mode='reflect').reshape(shape_size)

    return distorted_image


