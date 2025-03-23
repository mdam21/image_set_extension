from ampliacion_lib.process_img import process_all_images
from ampliacion_lib.utils import move_images, update_json
import numpy as np
import os

def main():
    """
        Función principal, encargada de gestionar los directorios y los tipos de filtros que se van a utilizar.
        Esto lo hace aplicando las configuraciones para cada filtro. Si no se modifica los valores no aplica el filtro.

    :return:
        Nada:   Crea los directorios ./amp_img/data/processed_images/temp_set/     - Carpetas temporales separadas por nombres de filtros.
                                                                                     Cada una contiene su propio .json

                                     ./amp_img/data/processed_images/total_set/    - carpeta final, reúne todas las imágenes de todas las carpetas
                                                                                     temporales y actualiza el .json final. El programa principal crea un error de conteo.
                                                                                     Utilizar el programa secundario. Comentada línea
    """

    # Parámetros para los filros a aplicar

    # Prefijo, nombre del set a tratar
    prefix_name = 'Accordion'

    # Indice de inicio
    cont_indice = 1

    # desenfoque
    blur_sigma = 2.5

    # canny
    thres1= 50
    thres2= 75

    # brillo
    brightness_percent = 50
    mode = 'positive' #Modo de brillo, configuración base both

    # contraste
    v_contrast_percentage = 40

    # cropping
    crop_perc = 0.5 # Porcentaje de recorte, entre 0 y 0.5

    # cutout
    num_squ = 5
    cutout_per = 15

    # Desenfoque selectivo de Gauss, utilizar factores de 10 para ver cambios significativos.
    #threshold_gauss = 90

    # Transformación elástica
    alph = 100
    sigm = 10

    # Exposición
    exp_perc = 50

    # flipping
    flip_option = "horizontal"  # Puede ser "horizontal", "vertical" o "both"

    # Gray scale
    g_scale = 100

    # Hue filtro
    hue_val = 150

    # Noise filtro
    noise_val = 0.25 # Porcentaje de ruido, entre 0 y 0.25 (equivale a 0% - 25%) PONER VALORES SOLO ENTRE 0-1.

    # Rotación
    r_angle = 15

    # saturacion
    saturation_percent = 80

    # Filtro Sepia:
    custom_filter = np.array([[0.393, 0.769, 0.189],  # Sepia para el canal Rojo
                              [0.349, 0.686, 0.168],  # Sepia para el canal Verde
                              [0.272, 0.534, 0.131]])  # Sepia para el canal Azul
    filter_name = "sepia"

    # Sobel
    apply_sobel = True

    # Mixture
    mix1 = True #blur-grayscale
    mix2 = True #contrast-brightness
    mix3 = True #saturation-brightness

    try:
        # Directorios
        image_dir = 'C:\\Users\\and_d\\OneDrive\\Escritorio\\Ubuntu\\data\\input_images\\Accordion\\'
        json_path = 'C:\\Users\\and_d\\OneDrive\\Escritorio\\Ubuntu\\data\\input_images\\Accordion\\Accordion.json'
        output_dir = 'C:\\Users\\and_d\\OneDrive\\Escritorio\\Ubuntu\\data\\processed_images\\temp_set\\'

        if 'blur_sigma' in locals():
            try:
                print("Aplicando filtro de desenfoque:")
                process_all_images(
                    image_dir, json_path, output_dir,
                    blur_sigma=blur_sigma
                )
                input("Filtro de desenfoque aplicado. Presiona 'Enter' para continuar.\n")
                tmp_blur_img_dir = os.path.join(output_dir, f"blur_{blur_sigma}")
            except Exception as e:
                print(f"Error al aplicar filtro de desenfoque: {e}")

        if 'thres1' in locals() and 'thres2' in locals():
            try:
                print("Aplicando filtro de bordes canny:")
                process_all_images(
                    image_dir, json_path, output_dir,
                    threshold1=thres1,
                    threshold2=thres2
                )
                input("Filtro de Bordes Canny aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicar filtro de bordes Canny: {e}")

        if 'brightness_percent' in locals():
            try:
                print("Aplicando ajuste de brillo:")
                process_all_images(
                    image_dir, json_path, output_dir,
                    brightness_percent=brightness_percent
                )
                tmp_bright_img_dir = os.path.join(output_dir, f"brightness_{brightness_percent}")
                input("Ajuste de brillo aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicar el filtro de brillo: {e}")

        if 'v_contrast_percentage' in locals():
            try:
                print("Aplicando ajuste de contraste:")
                process_all_images(
                    image_dir, json_path, output_dir,
                    contrast_percent=v_contrast_percentage
                )
                tmp_contrast_img_dir = os.path.join(output_dir, f"contrast_{v_contrast_percentage}")
                input("Ajuste de contraste aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicar el filtro de contraste: {e}")

        if 'crop_perc' in locals():
            try:
                print("Aplicando filtro de corte con porcenntaje:")
                process_all_images(
                    image_dir, json_path, output_dir,
                    crop_percent=crop_perc
                )
                input("Ajuste de cropping aplicado. Presiona 'Enter' para continuar\n")
            except Exception as e:
                print(f"Error al aplicar filtro de corte con porcentaje: {e}")

        if 'cutout_per' in locals() and 'num_squ' in locals():
            try:
                print("Aplicando CutOut:")
                process_all_images(
                    image_dir, json_path, output_dir,
                    cutout_percent=cutout_per,
                    num_squares=num_squ
                )
                input("Ajuste de CutOut aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicar filtro de CutOut: {e}")

        if 'threshold_gauss' in locals():
            try:
                print("Aplicando desenfoque selectivo de Gauss:")
                process_all_images(
                    image_dir, json_path, output_dir,
                    threshold=threshold_gauss
                )
                input("Ajuste de Desenfoque Selectivo aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicar filtro de Desenfoque selectivo de Gauss: {e}")

        if 'alph' and 'sigm' in locals():
            try:
                print("Aplicando filtro de elasticidad:")
                process_all_images(
                    image_dir, json_path, output_dir,
                    alpha=alph,
                    sigma=sigm
                )
                input("Ajuste de elasticidad aplicado. Presione 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicar filtro de Elasticidad: {e}")

        if 'exp_perc' in locals():
            try:
                print("Aplicando ajuste de exposición:")
                process_all_images(image_dir, json_path, output_dir,
                    exposure_percent=exp_perc
                )
                input("Filtro de Exposición aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicar filtro de Exposición: {e}")

        if 'flip_option' in locals():
            try:
                print("Aplicando giro:")
                process_all_images(image_dir, json_path, output_dir,
                    how=flip_option
                )
                input("Filtro de Flip aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicar el filtro de Flip: {e}")

        if 'g_scale' in locals():
            try:
                print("Aplicando escala de grises")
                process_all_images(image_dir, json_path, output_dir,
                    grayscale_percent=g_scale
                )
                input("Filtro de Gray Scale aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicar el filtro de Escala de Grises: {e}")

        if 'hue_val' in locals():
            try:
                print("Aplicando filtro HUE")
                process_all_images(image_dir, json_path, output_dir,
                    max_hue_shift_degrees=hue_val
                )
                input("Filtro de HUE aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicar el filtro de Escala de HUE: {e}")

        if 'noise_val' in locals():
            try:
                print("Aplicando filtro noise:")
                process_all_images(image_dir, json_path, output_dir,
                    noise_amount=noise_val
                )
                input("Filtro de ruido aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicare le filtro de Ruido. {e}")

        if 'r_angle' in locals():
            try:
                print("Aplicando filtro de rotación:")
                process_all_images(
                    image_dir, json_path, output_dir,
                    rotation_angle=r_angle
                )
                input("Filtro de rotación arbitraria aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicare le filtro de Ruido. {e}")

        """
        Código para hacer rotación de 90°, no incluido, problemas con los .json generados.
        if 'rot_side' in locals():
            try:
                print("Aplicando filtro de rotación de lado")
                process_all_images(
                    image_dir, json_path, output_dir,
                    rotation_angle=rot_side
                )
                input("Ajuste de rotación de lado aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicare le filtro de Rotación de lado. {e}")

        """

        if 'saturation_percent' in locals():
            try:
                print("Aplicando ajuste de saturación:")
                process_all_images(
                    image_dir, json_path, output_dir,
                    saturation_percent=saturation_percent
                )
                input("Ajuste de saturación aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicare le filtro de Saturación. {e}")

        if 'filter_name' in locals():
            try:
                if custom_filter is not None:
                    print(f"Aplicando filtro sepia:")
                    process_all_images(
                        image_dir, json_path, output_dir,
                        custom_filter=custom_filter,
                        filter_name=filter_name
                    )
                    input(f"Filtro {filter_name} aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicare le filtro Sepia. {e}")

        if 'apply_sobel' in locals():
            try:
                print("Aplicando filtro Sobel:")
                process_all_images(
                    image_dir, json_path, output_dir,
                    apply_sobel=True
                )
                input("Filtro Sobel aplicado. Presiona 'Enter' para continuar.\n")
            except Exception as e:
                print(f"Error al aplicare le filtro Sepia. {e}")

        if 'mix1' in locals():
            try:
                print("Mezcla de filtro Blur + Grayscale")
                # Buscar el archivo .json en el directorio temporal de salida (tmp_blur_img_dir)
                json_files = [f for f in os.listdir(tmp_blur_img_dir) if f.endswith(".json")]

                if not json_files:
                    raise FileNotFoundError(f"No se encontró ningún archivo .json en el directorio {tmp_blur_img_dir}")

                tmp_json_path = os.path.join(tmp_blur_img_dir, json_files[0])

                # Procesar las imágenes con el filtro Grayscale
                process_all_images(
                    tmp_blur_img_dir, tmp_json_path, output_dir,
                    grayscale_percent=g_scale,
                    mix1=True
                )

                input("Mezcla de Blur + Grayscale aplicada. Presiona 'Enter' para continuar.\n")

            except Exception as e:
                print(f"Error al aplicar la mezcla de Blur + Grayscale: {e}")

        if 'mix2' in locals():
            try:
                print("Mezcla de filtro Contrast + Brightness:")
                json_files = [f for f in os.listdir(tmp_contrast_img_dir) if f.endswith(".json")]

                if not json_files:
                    raise FileNotFoundError(f"No se encontró ningún archivo .json en el directorio {tmp_contrast_img_dir}")

                tmp_json_path = os.path.join(tmp_contrast_img_dir, json_files[0])

                # Procesar las imágenes con el filtro Grayscale
                process_all_images(
                    tmp_contrast_img_dir, tmp_json_path, output_dir,
                    brightness_percent=brightness_percent,
                    mix2=True
                )

            except Exception as e:
                print(f"Error al aplicar la mezcla de Contrast + Brightness: {e}")

        if 'mix3' in locals():
            try:
                print("Mezcla de filtro Saturation + Brightness:")
                json_files = [f for f in os.listdir(tmp_bright_img_dir) if f.endswith(".json")]

                if not json_files:
                    raise FileNotFoundError(f"No se encontró ningún archivo .json en el directorio {tmp_bright_img_dir}")

                tmp_json_path = os.path.join(tmp_bright_img_dir, json_files[0])

                # Procesar las imágenes con el filtro Grayscale
                process_all_images(
                    tmp_bright_img_dir, tmp_json_path, output_dir,
                    saturation_percent=saturation_percent,
                    mix3=True
                )

            except Exception as e:
                print(f"Error al aplicar la mezcla de Contrast + Brightness: {e}")

        subdirs = []

        if 'blur_sigma' in locals():
            subdirs.append(os.path.join(output_dir, f"blur_{blur_sigma}"))
        if 'thres1' in locals() and 'thres2' in locals():
            subdirs.append(os.path.join(output_dir, f"canny_{thres1}_{thres2}"))
        if 'brightness_percent' in locals():
            subdirs.append(os.path.join(output_dir, f"brightness_{brightness_percent}"))
        if 'Mix1' in locals():
            subdirs.append(os.path.join(output_dir, f"blur_gray_{Mix1}"))
        if 'Mix2' in locals():
            subdirs.append(os.path.join(output_dir, f"contrast_brightness_{Mix2}"))
        if 'Mix3' in locals():
            subdirs.append(os.path.join(output_dir, f"saturation_brightness_{Mix3}"))
        if 'crop_perc' in locals():
            subdirs.append(os.path.join(output_dir, f"cropping_{crop_perc}"))
        if 'cutout_per' in locals() and 'num_squ' in locals():
            subdirs.append(os.path.join(output_dir, f"cutout_{cutout_per}_{num_squ}"))
        if 'threshold_gauss' in locals():
            subdirs.append(os.path.join(output_dir, f"gauss_sel_{threshold_gauss}"))
        if 'alph' in locals() and 'sigm' in locals():
            subdirs.append(os.path.join(output_dir, f"elastic_{alph}_{sigm}"))
        if 'exp_perc' in locals():
            subdirs.append(os.path.join(output_dir, f"exposure_{exp_perc}"))
        if 'flip_option' in locals():
            subdirs.append(os.path.join(output_dir, f"flip_{flip_option}"))
        if 'g_scale' in locals():
            subdirs.append(os.path.join(output_dir, f"gray_scale_{g_scale}"))
        if 'hue_val' in locals():
            subdirs.append(os.path.join(output_dir, f"hue_{hue_val}"))
        if 'noise_val' in locals():
            subdirs.append(os.path.join(output_dir, f"noise_{noise_val}"))
        if 'r_angle' in locals():
            subdirs.append(os.path.join(output_dir, f"rotation_{r_angle}"))
        if 'rot_side' in locals():
            subdirs.append(os.path.join(output_dir, f"rotation_{rot_side}"))
        if 'saturation_percent' in locals():
            subdirs.append(os.path.join(output_dir, f"saturation_{saturation_percent}"))
        if 'filter_name' in locals():
            subdirs.append(os.path.join(output_dir, filter_name))

        #if subdirs:
            #try:
            #    print("Moviendo imágenes procesadas y actualizando .json")

                # Primero, mover las imágenes y actualizar el índice
                #img_index = move_images(subdirs, total_output_dir, cont_indice, prefix_name)

                # Ahora actualizar el JSON con el nuevo índice
                #img_index = update_json(subdirs, total_json_path, img_index, prefix_name)

            #   print(f"Proceso completado. {img_index - 1} imágenes procesadas y JSON actualizado.")
            #except Exception as e:
            #    print(f"Error al mover las imágenes o actualizar el .json. {e}")

    except FileNotFoundError as fnf_error:
        print(f"Archivo no encontrado: {fnf_error}")
    except PermissionError as perm_error:
        print(f"Permiso denegado: {perm_error}")
    except Exception as general_error:
        print(f"Ocurrió un error inesperado: {general_error}")

"""
# Verificar si hay subdirectorios para procesar
    if subdirs:
        try:
            

        except FileNotFoundError as fnf_error:
            print(f"Archivo no encontrado: {fnf_error}")
        except PermissionError as perm_error:
            print(f"Permiso denegado: {perm_error}")
        except Exception as general_error:
            print(f"Ocurrió un error inesperado: {general_error}")
"""
if __name__ == "__main__":
    main()
