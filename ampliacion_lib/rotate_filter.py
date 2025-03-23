
import cv2

def first_rotate_image(img, angle):
    """
        Rota una imagen en un ángulo dado.

    Parámetros:
        img - array: Imagen en arreglo a rotar.
        angle - float: Ángulo de rotación.

    Retorna:
        rotated_img - array: Imagen rotada.
    """
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    return rotated_img


