import cv2

def apply_canny_filter(img, threshold1=100, threshold2=200):
    """
        Aplica el filtro de detección de bordes Canny a una imagen, para esto utilizamos la librería cv2
        con el módulo .cvtColor y .Canny para transformar a escala de grises de ser necesario y para procesar
        los bordes.

    Parámetros:
        img - array: Imagen original.
        threshold1 - int: valor mínimo para detección de bordes.
        threshold2 - int: valor máximo para detección de bordes.

    Retorna:
        edges - array: Imagen procesada con bordes marcados.
    """
    # Convertir la imagen a escala de grises si está en color
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar el filtro Canny para la detección de bordes
    edges = cv2.Canny(img, threshold1, threshold2)

    return edges


