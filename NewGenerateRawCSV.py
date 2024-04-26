import os
import csv
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter import filedialog

def process_files(folder_path):
    global max_lines
    max_lines = 0
    global headers_list
    headers_list = []
    global aux_keys
    aux_keys = []
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
    
    aux_keys.remove("File")
    aux_keys.remove("Component")
    aux_keys.sort()
    aux_keys.insert(0, "Component")
    headers_list = headers_list + aux_keys

    return data

def process_file(file_path):
    global max_lines
    global headers_list
    global aux_keys
    print("Procesando archivo:", file_path)
    # Leer el contenido del archivo
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Inicializar una lista para almacenar los datos del archivo
    file_data = []
    temp_data = {"File":file.name.split("\\")[-1]}
    # Iterar sobre cada línea del archivo y extraer los datos relevantes
    component = ""
    for line in lines:
        # Limpiar la línea y extraer los datos relevantes
        line = line.strip()
        if "\n" in line:
            line = line.replace("\n", "")
        if '"' in line:
            line = line.replace('"', "")
        if "'" in line:
            line = line.replace("'", "")

        if line == "END":
            break
        elif line:
            if ":" in line:
                key, value = line.split(":", 1)
                temp_data[key.strip()] = value.strip()
            elif "," in line:
                continue
            else:
                # Si no hay un ":" o "," en la línea, solo la agregamos a los datos del archivo
                if 'Text' not in file_data:
                    temp_data['Text'] = line
                else:
                    temp_data['Text'] += " " + line
    file_data.append(temp_data)

    if len(temp_data.keys()) > max_lines:
        max_lines = len(temp_data.keys())
        headers_list = list(temp_data.keys())

    for line in lines:
        temp_data = {"File":file.name.split("\\")[-1],"Component":""}
        # Limpiar la línea y extraer los datos relevantes
        line = line.strip()
        if "\n" in line:
            line = line.replace("\n", "")
        if '"' in line:
            line = line.replace('"', "")
        if "'" in line:
            line = line.replace("'", "")

        if line == "END":
            break
        elif line:
            if "," in line:
                value, key = line.split(",", 1)
                if "StartComponent" in key:
                    component = key
                elif "EndComponent" in key:
                    component = ""
                elif key not in temp_data:
                    temp_data[key] = value
                temp_data["Component"] = component
                file_data.append(temp_data)

        for key in temp_data.keys():
            if key not in aux_keys:
                aux_keys.append(key)

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
    global headers_list
    folder_path = folder_path_entry.get()

    if not folder_path:
        # Si no se ha seleccionado una carpeta, mostrar una ventana de error
        tk.messagebox.showerror("Error", "Por favor selecciona una carpeta.")
        return
    
    # Procesar los archivos y obtener los datos
    data = process_files(folder_path)

    data2 = []
    for lista in data:
        for file_data in lista:
            data2.append(file_data)

    # Generar el nombre de archivo con la fecha actual
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Construir ruta del archivo en la carpeta seleccionada
    output_file = os.path.join(folder_path, f"datos_{current_date}.csv")  

    headers = headers_list

    # Escribir los datos en un archivo CSV
    write_to_csv(headers, data2, output_file)

    print("¡Conversión completa! Los datos se han guardado en", output_file)

def browse_folder():
    global folder_path
    folder_selected = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_selected)

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
