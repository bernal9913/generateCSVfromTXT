import os
import csv
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

def process_files(folder_path, selected_files=None):
    global max_lines
    max_lines = 0
    global headers_list
    headers_list = []
    global aux_keys
    aux_keys = []
    data = []

    # Si no se seleccionaron archivos específicos, procesar todos los archivos de la carpeta
    if not selected_files:
        selected_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    for filename in selected_files:
        file_path = os.path.join(folder_path, filename)
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

    with open(file_path, 'r') as file:
        lines = file.readlines()

    file_data = []
    temp_data = {"File": file.name.split("\\")[-1]}
    component = ""
    for line in lines:
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
                if 'Text' not in file_data:
                    temp_data['Text'] = line
                else:
                    temp_data['Text'] += " " + line
    file_data.append(temp_data)

    if len(temp_data.keys()) > max_lines:
        max_lines = len(temp_data.keys())
        headers_list = list(temp_data.keys())

    for line in lines:
        temp_data = {"File": file.name.split("\\")[-1], "Component": ""}
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

def write_to_csv(headers, data, output_file, mode='w'):
    with open(output_file, mode=mode, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        if mode == 'w':
            writer.writeheader()
        for file_data in data:
            writer.writerow(file_data)

def generate_csv():
    global folder_path
    global headers_list
    folder_path = folder_path_entry.get()

    if not folder_path:
        tk.messagebox.showerror("Error", "Por favor selecciona una carpeta.")
        return

    # Preguntar si procesar todos los archivos o elegir específicos
    process_all = messagebox.askyesno("Seleccionar Archivos", "¿Quieres procesar todos los archivos de la carpeta?")

    selected_files = None
    if not process_all:
        selected_files = filedialog.askopenfilenames(initialdir=folder_path, filetypes=[("Text files", "*.txt")])
        selected_files = [os.path.basename(file) for file in selected_files]

    data = process_files(folder_path, selected_files)

    data2 = []
    for lista in data:
        for file_data in lista:
            data2.append(file_data)

    export_type = messagebox.askquestion("Tipo de Exportación", "¿Es una exportación inicial (Sí) o una actualización (No)?")

    if export_type == 'yes':
        mode = 'w'
    else:
        mode = 'a'
        output_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not output_file:
            tk.messagebox.showerror("Error", "No se seleccionó ningún archivo CSV para actualizar.")
            return

    if mode == 'w':
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(folder_path, f"datos_{current_date}.csv")

    headers = headers_list
    write_to_csv(headers, data2, output_file, mode)

    print("¡Conversión completa! Los datos se han guardado en", output_file)

def browse_folder():
    global folder_path
    folder_selected = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_selected)

root = tk.Tk()
ttk.Style().configure('Gray.TButton', foreground='black', background='gray')
root.title("Seleccionar Campos para CSV")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)

browse_button = ttk.Button(root, text="Seleccionar Carpeta", command=browse_folder)
browse_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

folder_path_entry = ttk.Entry(root)
folder_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

generate_button = ttk.Button(root, text="Generar CSV", command=generate_csv, style="Gray.TButton")
generate_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

root.onexit = root.destroy

root.mainloop()
