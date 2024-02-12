import os
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


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
        for file_data in data:
            writer.writerow(file_data)


def generate_csv():
    global folder_path
    folder_path = folder_path_entry.get()

    # Obtener los campos seleccionados por el usuario
    selected_fields = [field for i, field in enumerate(all_fields) if field_comboboxes[i].get() == "Si"]

    # Procesar los archivos y obtener los datos
    data = process_files(folder_path)
    headers = verify_data(data, selected_fields)

    data2 = []
    for file_data in data:
        new_file_data = {}
        for key in file_data.keys():
            if key in headers:
                new_file_data[key] = file_data[key]
            elif key not in headers and key in selected_fields:
                new_file_data[key] = ""
        data2.append(new_file_data)

    # Escribir los datos en un archivo CSV
    output_file = "datos.csv"
    write_to_csv(headers, data2, output_file)

    print("¡Conversión completa! Los datos se han guardado en", output_file)


def verify_data(data, selected_fields):
    # Verificar que los datos sean correctos
    headers = []
    for file_data in data:
        for key in file_data.keys():
            if key not in headers and key in selected_fields:
                headers.append(key)
    return headers


def change_all_fields(value):
    if value == "Si":
        for field_var in field_comboboxes:
            field_var.set("Si")
    elif value == "No":
        for field_var in field_comboboxes:
            field_var.set("No")


def browse_folder():
    global folder_path
    folder_selected = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_selected)


# Crear la interfaz gráfica
root = tk.Tk()
root.title("Seleccionar Campos para CSV")

# Obtener la ruta del directorio actual donde se encuentra el script
folder_path = "."  # Puedes usar el directorio actual como predeterminado
datos = process_files(folder_path)
all_fields = []
for file_data in datos:
    for key in file_data.keys():
        if key not in all_fields:
            all_fields.append(key)

# Botón para seleccionar la carpeta
browse_button = ttk.Button(root, text="Seleccionar Carpeta", command=browse_folder)
browse_button.grid(row=0, column=0, padx=5, pady=5)

# Entrada de texto para la ruta de la carpeta
folder_path_entry = ttk.Entry(root)
folder_path_entry.grid(row=0, column=1, padx=5, pady=5)

# Crear etiquetas y cuadros combinados para cada campo
field_comboboxes = []
selected_fields = []
for i, field in enumerate(all_fields):
    label = ttk.Label(root, text=field)
    label.grid(row=i + 1, column=0, padx=5, pady=5)

    field_var = tk.StringVar(value="Si")  # Valor predeterminado seleccionado
    combobox = ttk.Combobox(root, values=["Si", "No"], textvariable=field_var, state="readonly")
    combobox.grid(row=i + 1, column=1, padx=5, pady=5)

    field_comboboxes.append(field_var)

# Botón para generar el CSV
generate_button = ttk.Button(root, text="Generar CSV", command=generate_csv)
generate_button.grid(row=len(all_fields) + 2, columnspan=2, padx=5, pady=10)

# Boton para cambiar todos los campos a "Si"
change_all_button = ttk.Button(root, text="Seleccionar Todos", command=lambda: change_all_fields("Si"))
change_all_button.grid(row=len(all_fields) + 3, columnspan=2, padx=5, pady=10)

# Boton para cambiar todos los campos a "No"
change_all_button2 = ttk.Button(root, text="Deseleccionar Todos", command=lambda: change_all_fields("No"))
change_all_button2.grid(row=len(all_fields) + 4, columnspan=2, padx=5, pady=10)

root.mainloop()
