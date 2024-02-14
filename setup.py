import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "include_files": ["R05_1Summary.txt","R05_6Summary.txt"], "excludes": []}

base = None
if sys.platform == "win32":
    base = "None"  # Si no deseas que aparezca la consola al ejecutar el programa, cambia esto a "None"

setup(
    name="Programa para convertir txt a csv",
    version="1.0",
    description="Programa hecho por el RatService: Jesus Zazueta y Jesus Ramirez",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
