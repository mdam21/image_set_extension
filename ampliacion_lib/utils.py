import os
import shutil
import json

def move_images(src_dirs, dest_dir, start_index, base_name):
    """
    Mueve las imágenes de todos los subdirectorios al directorio destino.
    Asigna un nuevo nombre a las imágenes usando el nombre base como prefijo y un índice continuo.

    Parámetros:
        src_dirs - lista: Lista de directorios de origen.
        dest_dir - str: Directorio donde se guardarán las imágenes.
        start_index - int: Índice de inicio para el renombrado.
        base_name - str: Prefijo que será parte del nombre de las imágenes renombradas.

    Retorna:
        img_count - int: Índice modificado después de haber movido todas las imágenes.
    """
    try:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        img_count = start_index
        for src_dir in src_dirs:
            if not os.path.exists(src_dir):
                print(f"Omitiendo. El directorio {src_dir} no existe.")
                continue

            # Procesar diferentes tipos de imágenes (.jpg, .jpeg, .png)
            for img_name in os.listdir(src_dir):
                if img_name.endswith(('.jpg', '.jpeg', '.png')):  # Acepta varios formatos
                    old_path = os.path.join(src_dir, img_name)
                    new_name = f"{base_name}_{img_count}.jpg"  # Nombrar con el base_name e índice
                    new_path = os.path.join(dest_dir, new_name)
                    try:
                        shutil.copy(old_path, new_path)
                        img_count += 1
                    except (IOError, OSError) as e:
                        print(f"Error al copiar {old_path} a {new_path}: {e}")
    except Exception as e:
        print(f"Ocurrió un error al mover imágenes: {e}")

    return img_count


def update_json(src_dirs, new_json_path, start_index, base_name):
    """
    Actualiza las referencias de las imágenes en el archivo .json, ajustando los nombres de las imágenes para reflejar
    el nuevo nombre en el set total, usando un nombre base como prefijo.

    Parámetros:
        src_dirs - lista: Lista de directorios origen, cada uno contiene su propio archivo .json.
        new_json_path - str: Ruta donde se guardará el nuevo archivo .json combinado.
        start_index - int: Índice de inicio para renombrar las imágenes en el .json.
        base_name - str: Nombre base que será el prefijo de las imágenes y las entradas en el archivo JSON.

    Retorna:
        img_count - int: Nuevo índice después de actualizar las imágenes en el archivo .json.
    """
    img_count = start_index
    combined_data = []

    try:
        for src_dir in src_dirs:
            # Buscar cualquier archivo .json en el directorio
            json_file_path = None
            for file in os.listdir(src_dir):
                if file.endswith('.json'):  # Encuentra cualquier archivo JSON
                    json_file_path = os.path.join(src_dir, file)
                    break  # Sale del bucle una vez que encuentra el archivo JSON

            if json_file_path and os.path.exists(json_file_path):
                # Leer el archivo JSON encontrado
                try:
                    with open(json_file_path, 'r') as f:
                        data = json.load(f)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error al leer o decodificar el archivo JSON {json_file_path}: {e}")
                    continue

                for item in data:
                    # Asegurar que el campo 'image' exista
                    if 'image' in item:
                        item['image'] = f"{base_name}_{img_count}.jpg"  # Renombrar la imagen en el JSON
                        combined_data.append(item)  # Añadir al conjunto de datos combinado
                        img_count += 1
            else:
                print(f"No se encontró archivo JSON en: {src_dir}")

        # Guardar el archivo JSON combinado
        try:
            with open(new_json_path, 'w') as f:
                json.dump(combined_data, f, indent=4)
        except (IOError, OSError) as e:
            print(f"Error al guardar el archivo JSON combinado en {new_json_path}: {e}")

    except Exception as e:
        print(f"Ocurrió un error al actualizar el archivo JSON: {e}")

    return img_count



# Ejemplo de uso del código actualizado
if __name__ == "__main__":
    # Rutas de carpetas de origen y destino
    src_dirs = ["/path/to/set1", "/path/to/set2", "..."]  # Ajusta con las rutas de tus sets de imágenes
    dest_dir = "/path/to/output/images"
    new_json_path = "/path/to/output/combined_annotations.json"

    # Índice inicial para renombrar las imágenes
    start_index = 1
    base_name = "Adhesive_tape"

    # Mover las imágenes y actualizar el JSON
    img_count = move_images(src_dirs, dest_dir, start_index, base_name)
    update_json(src_dirs, new_json_path, start_index, base_name)

    print(f"Proceso completado. {img_count - 1} imágenes procesadas.")
