from .blur_filter import apply_blur_filter
from .bordes_canny_f import apply_canny_filter
from .brightness_f import apply_brightness_filter
from .cropping_f import crop_image
from .contrast_f import apply_contrast_filter
from .cutout_f import apply_cutout_filter
from .des_gauss_selec import apply_selective_gaussian_blur
from .elastic_f import elastic_transform
from .exposure_f import apply_exposure_filter
from .flipping_f import apply_flip_image
from .gray_scale_f import first_apply_grayscale_filter
from .hue_f import apply_hue_filter
#from .mix_blur_grayscale_f import apply_blur_filter as apply_mix_blur, apply_grayscale_filter
from .mix_saturation_brightness_f import apply_saturation_filter, apply_combined_filter
from .noise_f import apply_noise_filter
from .rotate_filter import first_rotate_image
from .rotation_f import rotate_image
from .saturation_f import apply_saturation_filter
from .sepia_f import apply_custom_filter
from .sobel_f import apply_sobel_filter


import os
import cv2
import json
import numpy as np
from PIL import Image

def apply_custom_filter(image, custom_filter):
    """
        Aplica un filtro de colores personalizado, para ello ocupa una matriz de transformación de colores. Esta es la
        función para aplicar el filtro sepia. Esta función no trabaja con imágenes en 2 tonos. O sea, no trabaja con b/n

    Parámetros:
        image - image PIL: Imagen.
        custom_filter - array: Matriz de 3x3 que transforma los valores de los 3 canales principales de la imagen pil.

    Retorna:
        filtered_img - image PIL: Imagen con filtro.
    """

    img_array = np.array(image)
    if img_array.shape[-1] == 3:
        filtered_img = img_array @ custom_filter.T
        filtered_img = np.clip(filtered_img, 0, 255)
    else:
        raise ValueError("La imagen debe tener 3 canales (RGB).")
    return Image.fromarray(filtered_img.astype('uint8'))

def update_annotations(annotation, start_x, start_y):
    """
        Para los giros de las imágenes también se debe tomar en cuenta las anotaciones del archivo .json.
        Esta función se encarga de actualizar las coordenadas de las anotaciones tras recortar la imagen.

    Parámetros:
        annotation - diccionario: Anotaciones originales de la imagen.
        start_x - int: Coordenada x de la esquina superior izquierda del recorte.
        start_y - int: Coordenada y de la esquina superior izquierda del recorte.

    Retorna:
        new_annotations - lista: Lista con las coordenadas modificadas.
    """
    new_annotations = []
    for box in annotation["annotations"]:
        label = box["label"]
        width = box["coordinates"]["width"]
        height = box["coordinates"]["height"]
        x = box["coordinates"]["x"]
        y = box["coordinates"]["y"]

        nX = x - start_x
        nY = y - start_y

        new_annotations.append({
            "label": label,
            "coordinates": {
                "x": nX,
                "y": nY,
                "width": width,
                "height": height
            }
        })
    return new_annotations

def update_flip_annotations(annotation, img_height, img_width, how):
    """
        Función que actualiza los valores de las coordenadas del archivo .json luego de voltear una imagen.

    Parámetros:
        annotation - diccionario: Diccionario de valores de la imágen original.
        img_height - int: Altura de la imagen original.
        img_width - int: Ancho de la imagen original.
        how - str: Dirección del volteo: 'horizontal', 'vertical' o 'both'.

    Retorna:
        list: Lista de valores actualizados con las nuevas coordenadas.
    """
    new_annotations = []
    for box in annotation["annotations"]:
        label = box["label"]
        width = box["coordinates"]["width"]
        height = box["coordinates"]["height"]
        x = box["coordinates"]["x"]
        y = box["coordinates"]["y"]

        if how == "vertical":
            nY = img_height - y
            nX = x
        elif how == "horizontal":
            nX = img_width - x
            nY = y
        elif how == "both":
            nX = img_width - x
            nY = img_height - y
        else:
            nX, nY = x, y

        new_annotations.append({
            "label": label,
            "coordinates": {
                "x": nX,
                "y": nY,
                "width": width,
                "height": height
            }
        })
    return new_annotations

def update_rotate_annotations(annotation, img_height, img_width, angle):
    """
        Función que actualiza los valores del archivo .json luego de recortar una imagen.

    Parámetros:
        annotation - diccionario: Valores  originales de la imagen.
        img_height - int: Altura de la imagen original.
        img_width - int: Anchura de la imagen original.
        angle - int: Ángulo de rotación SOLO FACTORES DE 90°.

    Retorna:
    list: Lista de anotaciones con las coordenadas actualizadas según la rotación.
    """
    new_annotations = []
    for box in annotation["annotations"]:
        label = box["label"]
        width = box["coordinates"]["width"]
        height = box["coordinates"]["height"]
        x = box["coordinates"]["x"]
        y = box["coordinates"]["y"]

        # Ajustar las coordenadas según el ángulo de rotación
        if angle == 90:
            nX = y
            nY = img_width - x
            nWidth = height
            nHeight = width
        elif angle == -90:
            nX = img_height - y
            nY = x
            nWidth = height
            nHeight = width
        elif angle == 180:
            nX = img_width - x
            nY = img_height - y
            nWidth = width
            nHeight = height
        else:
            nX, nY, nWidth, nHeight = x, y, width, height

        new_annotations.append({
            "label": label,
            "coordinates": {
                "x": nX,
                "y": nY,
                "width": nWidth,
                "height": nHeight
            }
        })
    return new_annotations

def process_all_images(image_dir, json_path, output_dir,
                       rotation_angle=None, blur_sigma=None,
                       threshold1=None, threshold2=None, threshold=None,
                       brightness_percent=None, contrast_percent=None, saturation_percent=None,
                       cutout_percent=None, num_squares=None,
                       alpha=None, sigma=None, exposure_percent=None,
                       how=None, grayscale_percent=None, max_hue_shift_degrees=None,
                       noise_amount=None, custom_filter=None, crop_percent=None,
                       filter_name=None, apply_sobel=None, mix1=None, mix2=None, mix3=None):
    """
        Función principal, va iterando por todos los filtros aplicándolos al set original de imágenes imagen por imagen.
        La mayoría
        Los sets se guardan en los directorios especificados.

    Parámetros:
        image_dir - str: Directorio de las imágenes originales.
        json_path - str: Ruta al .json original.
        output_dir - str: Directorio donde se guardarán las imágenes procesadas y el .json.
    """
    filter_dir = None

    # Condicionales basándose en la existencia o no de la variable que ocupa el filtro
    if blur_sigma is not None and blur_sigma > 0:
        filter_dir = os.path.join(output_dir, f"blur_{blur_sigma}")
    elif threshold1 is not None and threshold2 is not None:
        filter_dir = os.path.join(output_dir, f"canny_{threshold1}_{threshold2}")
    elif brightness_percent is not None and mix2 is None:
        filter_dir = os.path.join(output_dir, f"brightness_{brightness_percent}")
    elif contrast_percent is not None and mix2 is None:
        filter_dir = os.path.join(output_dir, f"contrast_{contrast_percent}")
    elif crop_percent is not None:
        filter_dir = os.path.join(output_dir, f"cropping_{crop_percent}")
    elif cutout_percent is not None and num_squares is not None:
        filter_dir = os.path.join(output_dir, f"cutout_{cutout_percent}_{num_squares}")
    elif threshold is not None:
        filter_dir = os.path.join(output_dir, f"gauss_sel_{threshold}")
    elif alpha is not None and sigma is not None:
        filter_dir = os.path.join(output_dir, f"elastic_{alpha}_{sigma}")
    elif exposure_percent is not None:
        filter_dir = os.path.join(output_dir, f"exposure_{exposure_percent}")
    elif how is not None:
        filter_dir = os.path.join(output_dir, f"flip_{how}")
    elif grayscale_percent is not None and mix1 is None:
        filter_dir = os.path.join(output_dir, f"gray_scale_{grayscale_percent}")
    elif max_hue_shift_degrees is not None:
        filter_dir = os.path.join(output_dir, f"hue_{max_hue_shift_degrees}")
    elif noise_amount is not None:
        filter_dir = os.path.join(output_dir, f"noise_{noise_amount}")
    elif rotation_angle is not None:
        filter_dir = os.path.join(output_dir, f"rotation_{rotation_angle}")
    elif saturation_percent is not None and mix3 is None:
        filter_dir = os.path.join(output_dir, f"saturation_{saturation_percent}")
    elif custom_filter is not None:
        filter_dir = os.path.join(output_dir, f"{filter_name}")
    elif mix1:
        filter_dir = os.path.join(output_dir, f"mix1_")
    elif mix2:
        filter_dir = os.path.join(output_dir, f"mix2_")
    elif mix3:
        filter_dir = os.path.join(output_dir, f"mix3_")
    elif apply_sobel:
        filter_dir = os.path.join(output_dir, f"sobel")
    else:
        print("No se especificó un filtro válido para aplicar.")
        return

    if filter_dir and not os.path.exists(filter_dir):
        os.makedirs(filter_dir)

    with open(json_path, 'r') as f:
        data = json.load(f)

    new_data = []

    for item in data:
        img_path = os.path.join(image_dir, item["image"])
        img = cv2.imread(img_path)
        if img is None:
            continue

        new_image_name = item['image']

        if blur_sigma is not None and blur_sigma > 0:
            img = apply_blur_filter(img, blur_sigma)
            new_image_name = f"blur_{blur_sigma}_{new_image_name}"

        elif threshold1 is not None and threshold2 is not None:
            img = apply_canny_filter(img, threshold1, threshold2)
            new_image_name = f"canny_{threshold1}_{threshold2}_{new_image_name}"

        elif brightness_percent is not None and mix2 is None:
            img = apply_brightness_filter(img, brightness_percent)
            new_image_name = f"brightness_{brightness_percent}_{new_image_name}"

        elif contrast_percent is not None and mix1 is None:
            img = apply_contrast_filter(img, contrast_percent)
            new_image_name = f"contrast_{contrast_percent}_{new_image_name}"

        elif crop_percent is not None:
            for annotation in item["annotations"]:
                x = annotation["coordinates"]["x"]
                y = annotation["coordinates"]["y"]
                width = annotation["coordinates"]["width"]
                height = annotation["coordinates"]["height"]

                img, (start_x, start_y) = crop_image(img, (x, y, width, height), crop_percent)
                new_image_name = f"cropped_{int(crop_percent * 100)}_{new_image_name}"

                new_annotations = update_annotations({"annotations": [annotation]}, start_x, start_y)

                new_data.append({
                    "image": new_image_name,
                    "annotations": new_annotations
                })

        elif cutout_percent is not None and num_squares is not None:
            img = apply_cutout_filter(img, num_squares, cutout_percent)
            new_image_name = f"cutout_{int(cutout_percent)}{num_squares}_{item['image'].split('.')[0]}.jpg"

        elif threshold is not None:
            img = apply_selective_gaussian_blur(img, threshold)
            new_image_name = f"des_gauss_{threshold}_{item['image'].split('.')[0]}.jpg"

        elif alpha is not None and sigma is not None:
            img = elastic_transform(img, alpha, sigma)
            new_image_name = f"elastic_{alpha}_{sigma}_{item['image'].split('.')[0]}.jpg"

        elif exposure_percent is not None:
            img = apply_exposure_filter(img, exposure_percent)
            new_image_name = f"exposure_{exposure_percent}_{item['image'].split('.')[0]}.jpg"

        elif how is not None:
            img_height, img_width = img.shape[:2]
            img = apply_flip_image(img, how)
            new_image_name = f"flipped_{how}_{new_image_name}"

        elif grayscale_percent is not None and mix1 is None:
            img = first_apply_grayscale_filter(img, grayscale_percent)
            new_image_name = f"gray_scale_{grayscale_percent}_{item['image'].split('.')[0]}.jpg"

        elif max_hue_shift_degrees is not None:
            img = apply_hue_filter(img, max_hue_shift_degrees)
            new_image_name = f"hue_{max_hue_shift_degrees}_{item['image'].split('.')[0]}.jpg"

        elif noise_amount is not None:
            img = apply_noise_filter(img, noise_amount)
            new_image_name = f"noise_{noise_amount}_{item['image'].split('.')[0]}.jpg"

        elif rotation_angle is not None:
            img_height, img_width = img.shape[:2]
            img = first_rotate_image(img, rotation_angle)
            new_image_name = f"rotated_{rotation_angle}_{new_image_name}"

        elif saturation_percent is not None and mix3 is None:
            img = apply_saturation_filter(img, saturation_percent)
            new_image_name = f"saturation_{saturation_percent}_{new_image_name}"

        elif custom_filter is not None:
            img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            img_pil = apply_custom_filter(img_pil, custom_filter)
            img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            new_image_name = f"{filter_name}_{new_image_name}"

        elif apply_sobel:
            img = apply_sobel_filter(
                img
            )
            new_image_name = f"sobel_{new_image_name}"

        if mix1 is not None:
            img = first_apply_grayscale_filter(
                img, grayscale_percent
            )
            new_image_name = f"blur_grayscale_{new_image_name}"

        if mix2 is not None:
            img = apply_brightness_filter(
                img, brightness_percent
            )

        if mix3 is not None:
            img = apply_saturation_filter(
                img, saturation_percent
            )

        if filter_dir:
            new_image_path = os.path.join(filter_dir, new_image_name)
            cv2.imwrite(new_image_path, img)

        if crop_percent is None:
            new_data.append({
                "image": new_image_name,
                "annotations": item["annotations"]
            })

    if filter_dir:
        new_json_path = os.path.join(filter_dir, "processed_images.json")
        with open(new_json_path, 'w') as f:
            json.dump(new_data, f, indent=4)

    print(f"Procesamiento completo para el filtro. Imágenes y anotaciones guardadas en: {filter_dir}")
