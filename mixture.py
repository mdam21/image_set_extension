import os
import shutil
import json


# Label del set de imágenes que se está ampliando. 
name = 'Accordion'

# Ruta de la carpeta raíz que contiene todas las carpetas con sus 200 imágenes y un .json
root_folder = 'C:\\Users\\and_d\\OneDrive\\Escritorio\\Ubuntu\\data\\processed_images\\temp_set\\'

# Ruta de la carpeta donde se almacenará el set completo.
output_image_dir = 'C:\\Users\\and_d\\OneDrive\\Escritorio\\Fin_amp\\data\\processed_images\\total_set\\'
output_json_file = 'C:\\Users\\and_d\\OneDrive\\Escritorio\\Fin_amp\\data\\processed_images\\total_set\\set_ampliado.json'


if not os.path.exists(output_image_dir):
    os.makedirs(output_image_dir)

consolidated_annotations = []

image_count = 1

input_folders = [os.path.join(root_folder, folder) for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))]

for folder in input_folders:
    json_file_path = None
    for file in os.listdir(folder):
        if file.endswith('.json'):
            json_file_path = os.path.join(folder, file)
            break  
            
    if json_file_path and os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            annotations = json.load(json_file)

            for annotation in annotations:
                image_filename = annotation['image']
                image_path = os.path.join(folder, image_filename)

                if os.path.exists(image_path):
                    new_image_filename = f'{name}_{image_count}.jpg'
                    new_image_path = os.path.join(output_image_dir, new_image_filename)

                    shutil.copy(image_path, new_image_path)

                    annotation['image'] = new_image_filename

                    consolidated_annotations.append(annotation)

                    image_count += 1
                else:
                    print(f"Imagen no encontrada: {image_path}")
    else:
        print(f"No se encontró archivo .json en: {folder}")

with open(output_json_file, 'w') as output_json:
    json.dump(consolidated_annotations, output_json, indent=4)

print(f"Proceso completado. Todas las imágenes se guardaron en: {output_image_dir}")
print(f"El archivo json juntado guardado en: {output_json_file}")
