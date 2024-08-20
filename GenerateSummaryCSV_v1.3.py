import os
import csv
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

def process_files(folder_path, selected_files=None):
    global format_type
    format_type = "Tipo Normal"
    global max_lines
    max_lines = 0
    global headers_list
    headers_list = []
    # Lista para almacenar los datos de todos los archivos
    data = []

    # Filtrar archivos según selección
    files_to_process = selected_files if selected_files else [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    # Verificar el tipo de formato con el primer archivo
    if files_to_process:
        file_path = os.path.join(folder_path, files_to_process[0])
        verify_format_type(file_path)

    # Procesar cada archivo seleccionado
    for filename in files_to_process:
        file_path = os.path.join(folder_path, filename)
        # Procesar cada archivo
        file_data = process_file(file_path)
        if file_data:
            data.append(file_data)

    return data

def verify_format_type(file_path):
    global format_type
    with open(file_path, 'r') as file:
        lines = file.readlines()

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
                break

def process_file(file_path):
    global format_type
    global max_lines
    global headers_list
    print("Procesando archivo:", file_path)
    # Leer el contenido del archivo
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Inicializar una lista para almacenar los datos del archivo
    file_data = {}

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

    if len(file_data) > max_lines:
        max_lines = len(file_data)
        headers_list = file_data.keys()

    return file_data

def write_to_csv(headers, data, output_file, mode='w'):
    # Escribir los datos en el archivo CSV
    with open(output_file, mode=mode, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        if mode == 'w':
            writer.writeheader()
        for file_data in data:
            writer.writerow(file_data)

def generate_csv():
    global headers_list
    global folder_path
    folder_path = folder_path_entry.get()

    if not folder_path:
        # Si no se ha seleccionado una carpeta, mostrar una ventana de error
        tk.messagebox.showerror("Error", "Por favor selecciona una carpeta.")
        return

    # Preguntar si se desean procesar todos los archivos o seleccionar archivos específicos
    process_all = messagebox.askyesno("Procesar Archivos", "¿Deseas procesar todos los archivos en la carpeta?")

    selected_files = []
    if not process_all:
        selected_files = filedialog.askopenfilenames(initialdir=folder_path, title="Selecciona Archivos", filetypes=[("Text files", "*.txt")])
        selected_files = [os.path.basename(f) for f in selected_files]  # Obtener solo los nombres de archivo

    # Obtener los campos seleccionados por el usuario
    selected_fields = [field for i, field in enumerate(headers_list) if field_comboboxes[i].get() == "Si"]

    # Procesar los archivos y obtener los datos
    data = process_files(folder_path, selected_files)
    headers = headers_list

    data2 = []
    for file_data in data:
        new_file_data = {}
        for key in file_data.keys():
            if key in headers:
                new_file_data[key] = file_data[key]
            elif key not in headers and key in selected_fields:
                new_file_data[key] = ""
        data2.append(new_file_data)

    # Preguntar al usuario si es una exportación inicial o una actualización
    export_type = messagebox.askquestion("Tipo de Exportación", "¿Es una exportación inicial (Sí) o una actualización (No)?")

    if export_type == 'yes':
        mode = 'w'  # Modo escritura (sobrescribe)
    else:
        mode = 'a'  # Modo agregar (append)
        # Seleccionar archivo CSV para actualizar
        output_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not output_file:
            tk.messagebox.showerror("Error", "No se seleccionó ningún archivo CSV para actualizar.")
            return

    if mode == 'w':
        # Generar el nombre de archivo con la fecha actual
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(folder_path, f"datos_{current_date}.csv")  # Construir ruta del archivo en la carpeta seleccionada

    # Escribir los datos en un archivo CSV
    write_to_csv(headers, data2, output_file, mode)

    print(f"¡Conversión completa! Los datos se han guardado en {output_file}")

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
        datos = process_files(folder_selected)

        # Limpiar el marco de campos antes de agregar nuevos elementos
        for widget in fields_frame.winfo_children():
            widget.destroy()

        # Crear etiquetas y cuadros combinados para cada campo
        global field_comboboxes
        field_comboboxes = []
        global headers_list
        for i, field in enumerate(headers_list):
            label = ttk.Label(fields_frame, text=field)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            field_var = tk.StringVar(value="Si")  # Valor predeterminado seleccionado
            combobox = ttk.Combobox(fields_frame, values=["Si", "No"], textvariable=field_var, state="readonly")
            combobox.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

            field_comboboxes.append(field_var)

# Crear la interfaz gráfica
root = tk.Tk()
ttk.Style().configure('Gray.TButton', foreground='black', background='gray')
root.title("Seleccionar Campos para CSV")

# Configurar el grid para que se expanda
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)  # La entrada de texto tendrá más espacio
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1)

# Botón para seleccionar la carpeta
browse_button = ttk.Button(root, text="Seleccionar Carpeta", command=browse_folder)
browse_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Entrada de texto para la ruta de la carpeta
folder_path_entry = ttk.Entry(root)
folder_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Botón para generar el CSV, color gris de fondo
generate_button = ttk.Button(root, text="Generar CSV", command=generate_csv, style="Gray.TButton")
generate_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

# Crear un marco para el panel de desplazamiento
scrollable_frame = ttk.Frame(root)
scrollable_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

# Configurar el grid para el marco de desplazamiento
scrollable_frame.grid_columnconfigure(0, weight=1)
scrollable_frame.grid_rowconfigure(0, weight=1)

# Configurar el panel de desplazamiento
scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical")
scrollbar.grid(row=0, column=1, sticky="ns")

# Configurar el lienzo dentro del panel de desplazamiento
canvas = tk.Canvas(scrollable_frame, yscrollcommand=scrollbar.set)
canvas.grid(row=0, column=0, sticky="nsew")

# Asociar el lienzo al panel de desplazamiento
scrollbar.config(command=canvas.yview)

# Crear un nuevo marco para contener los campos
fields_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=fields_frame, anchor="nw")

# Configurar el panel de desplazamiento para expandirse con el tamaño del contenido
fields_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Permitir que el lienzo y el marco de campos se expandan al cambiar el tamaño de la ventana
canvas.grid_columnconfigure(0, weight=1)
canvas.grid_rowconfigure(0, weight=1)
fields_frame.grid_columnconfigure(0, weight=1)
fields_frame.grid_rowconfigure(0, weight=1)

# Permitir el desplazamiento con la rueda del ratón
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

root.onexit = root.destroy

root.mainloop()
