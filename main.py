import os
import csv

def process_files(folder_path):
    # Lista para almacenar los datos de todos los archivos
    data = []

    # Iterar sobre todos los archivos en la carpeta
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            # Procesar cada archivo
            file_data = process_file(file_path)
            if file_data:
                data.append(file_data)

    return data

def process_file(file_path):
    print("Procesando archivo:", file_path)
    # Leer el contenido del archivo
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Inicializar un diccionario para almacenar los datos del archivo
    file_data = {
        "Subject": "",
        "Session": "",
        "Responses on Lever 1": "",
        "Response rate on Lever 1": "",
        "Responses on Lever 2": "",
        "Response rate on Lever 2": "",
        "Reinforcers on Lever 1": "",
        "Reinforcer rate on Lever 1": "",
        "Reinforcers on Lever 2": "",
        "Reinforcer rate on Lever 2": "",
        "Total time in minutes": "",
        "COM Port": "",
        "Lever 1 Schedule": "",
        "Lever 2 Schedule": ""
    }

    # Variable para rastrear si se ha encontrado la primera línea de datos
    found_first_line = False

    # Iterar sobre cada línea del archivo y extraer los datos relevantes
    for line in lines:
        if found_first_line:
            if line.strip() == "END":
                break  # Terminar la lectura del archivo al encontrar "END"
            elif line.strip() == "":
                continue  # Saltar líneas vacías
            if ":" in line:
                key, value = line.split(":", 1)
                file_data[key.strip().replace('"', '')] = value.strip().replace('"', '')
        elif line.strip() == "END":
            break
        else:
            found_first_line = True

    return file_data

def write_to_csv(data, output_file):
    # Definir los nombres de las columnas para el archivo CSV
    fieldnames = ["Subject", "Session", "Responses on Lever 1", "Response rate on Lever 1",
                  "Responses on Lever 2", "Response rate on Lever 2", "Reinforcers on Lever 1",
                  "Reinforcer rate on Lever 1", "Reinforcers on Lever 2", "Reinforcer rate on Lever 2",
                  "Total time in minutes", "COM Port", "Lever 1 Schedule", "Lever 2 Schedule"]

    # Escribir los datos en el archivo CSV
    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Obtener la ruta del directorio actual donde se encuentra el script
script_dir = os.path.dirname(os.path.realpath(__file__))
folder_path = script_dir  # Usar el directorio actual como la carpeta de archivos

# Procesar los archivos y obtener los datos
data = process_files(folder_path)

# Escribir los datos en un archivo CSV
output_file = "datos.csv"
write_to_csv(data, output_file)

print("¡Conversión completa! Los datos se han guardado en", output_file)
