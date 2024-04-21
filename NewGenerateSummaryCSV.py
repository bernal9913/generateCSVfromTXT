import os
import csv
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter import filedialog

all_fields = []
format_type = "Tipo Normal"
headers_list = []

def process_files(folder_path):
    # Lista para almacenar los datos de todos los archivos
    data = []

    # Iterar sobre todos los archivos en la carpeta
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            verify_format_type(file_path)
            break

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            # Procesar cada archivo
            file_data = process_file(file_path)
            if file_data:
                data.append(file_data)

    return data

def verify_format_type(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            if value == "":
                format_type = "Tipo Seccionado"
                break

def process_file(file_path):
    global format_type
    print("Procesando archivo:", file_path)
    # Leer el contenido del archivo
    with open(file_path, 'r') as file:
        lines = file.readlines()


    # Inicializar una lista para almacenar los datos del archivo
    file_data = {}

    for line in lines:
        line = line.strip()
        if "\n" in line:
            line = line.replace("\n", "")
        if '"' in line:
            line = line.replace('"', "")
        if ":" in line:
            key, value = line.split(":", 1)
            if value == "":
                format_type = "Tipo Seccionado"

    print("Formato del archivo:", format_type)
    if format_type == "Tipo Normal":
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
    
    elif format_type == "Tipo Seccionado":
        # Iterar sobre cada línea del archivo y extraer los datos relevantes
        n = 1
        aux_key = ""
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
                if "Schedule" in line:
                    key, value = line.split(":", 1)
                    key = key + " Component " + str(n)
                    if "Lever 2" in key:
                        n += 1
                    file_data[key.strip()] = value.strip()
                elif ":" in line:
                    key, value = line.split(":", 1)
                    if value == "":
                        aux_key = key
                        continue
                    if "Component" in key:
                        key = aux_key + " " + key
                        file_data[key.strip()] = value.strip()
                    else:
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

    if not folder_path:
        # Si no se ha seleccionado una carpeta, mostrar una ventana de error
        tk.messagebox.showerror("Error", "Por favor selecciona una carpeta.")
        return

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

    # Generar el nombre de archivo con la fecha actual
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(folder_path, f"datos_{current_date}.csv")  # Construir ruta del archivo en la carpeta seleccionada

    # Escribir los datos en un archivo CSV
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

    if folder_selected:
        global all_fields
        datos = process_files(folder_selected)
        all_fields = []
        for file_data in datos:
            for key in file_data.keys():
                if key not in all_fields:
                    all_fields.append(key)
        # Crear etiquetas y cuadros combinados para cada campo
        global field_comboboxes
        field_comboboxes = []
        for i, field in enumerate(all_fields):
            label = ttk.Label(root, text=field)
            label.grid(row=i + 1, column=0, padx=5, pady=5)

            field_var = tk.StringVar(value="Si")  # Valor predeterminado seleccionado
            combobox = ttk.Combobox(root, values=["Si", "No"], textvariable=field_var, state="readonly")
            combobox.grid(row=i + 1, column=1, padx=5, pady=5)

            field_comboboxes.append(field_var)

# Crear la interfaz gráfica
root = tk.Tk()
ttk.Style().configure('Gray.TButton', foreground='black', background='gray')
root.title("Seleccionar Campos para CSV")

# Botón para seleccionar la carpeta
browse_button = ttk.Button(root, text="Seleccionar Carpeta", command=browse_folder)
browse_button.grid(row=0, column=0, padx=5, pady=5)

# Entrada de texto para la ruta de la carpeta
folder_path_entry = ttk.Entry(root)
folder_path_entry.grid(row=0, column=1, padx=5, pady=5)

# Botón para generar el CSV, color gris de fondo
generate_button = ttk.Button(root, text="Generar CSV", command=generate_csv, style="Gray.TButton")
generate_button.grid(row=0, column=2, padx=5, pady=5)

root.onexit = root.destroy

root.mainloop()
