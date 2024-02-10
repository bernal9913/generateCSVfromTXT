import os
import csv
import tkinter as tk
from tkinter import ttk

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

    # Inicializar una lista para almacenar los datos del archivo
    file_data = {}

    # Iterar sobre cada línea del archivo y extraer los datos relevantes
    for line in lines:
        # Limpiar la línea y extraer los datos relevantes
        line = line.strip()
        if "\n" in line:
            line = line.replace("\n", "")
        if '"' in line:
            line = line.replace('"', "")

        if line == "END":
            break
        elif line:
            if ":" in line:
                key, value = line.split(":", 1)
                file_data[key.strip()] = value.strip()
            else:
                # Si no hay un ":" en la línea, solo la agregamos a los datos del archivo
                if 'Text' not in file_data:
                    file_data['Text'] = line
                else:
                    file_data['Text'] += " " + line

    return file_data

def write_to_csv(headers, data, output_file):
    # Escribir los datos en el archivo CSV
    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

def generate_csv():
    # Obtener los campos seleccionados por el usuario
    selected_fields = [field.get() for field in field_comboboxes]

    # Procesar los archivos y obtener los datos
    data = process_files(folder_path)
    headers = verify_data(data, selected_fields)

    # Escribir los datos en un archivo CSV
    output_file = "datos.csv"
    write_to_csv(headers, data, output_file)

    print("¡Conversión completa! Los datos se han guardado en", output_file)

def verify_data(data, selected_fields):
    # Verificar que los datos sean correctos
    headers = []
    for file_data in data:
        for key in file_data.keys():
            if key not in headers and key in selected_fields:
                headers.append(key)
    return headers

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Seleccionar Campos para CSV")

# Obtener la ruta del directorio actual donde se encuentra el script
script_dir = os.path.dirname(os.path.realpath(__file__))
folder_path = script_dir  # Usar el directorio actual como la carpeta de archivos

# Crear una lista de campos disponibles
data = process_files(folder_path)
all_fields = []
for file_data in data:
    for key in file_data.keys():
        if key not in all_fields:
            all_fields.append(key)

# Crear etiquetas y cuadros combinados para cada campo
field_comboboxes = []
for i, field in enumerate(all_fields):
    label = ttk.Label(root, text=field)
    label.grid(row=i, column=0, padx=5, pady=5)

    field_var = tk.StringVar(value="Si")  # Valor predeterminado seleccionado
    combobox = ttk.Combobox(root, values=["Si", "No"], textvariable=field_var, state="readonly")
    combobox.grid(row=i, column=1, padx=5, pady=5)

    field_comboboxes.append(field_var)

# Botón para generar el CSV
generate_button = ttk.Button(root, text="Generar CSV", command=generate_csv)
generate_button.grid(row=len(all_fields), columnspan=2, padx=5, pady=10)

root.mainloop()
