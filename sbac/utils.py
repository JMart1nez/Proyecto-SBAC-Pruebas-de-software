import os
import json
import time
from datetime import datetime

# --- CONSTANTES DE RUTA ---
# Definimos dónde se guardará todo para no repetir texto en el código.
SBAC_DIR = ".sbac"            # Carpeta principal del sistema
COMMITS_DIR = os.path.join(SBAC_DIR, "commits")  # Donde viven las versiones
INDEX_FILE = os.path.join(SBAC_DIR, "index.json") # Lista de archivos a trackear
BASELINES_FILE = os.path.join(SBAC_DIR, "baselines.json") # Diccionario de líneas base
HEAD_FILE = os.path.join(SBAC_DIR, "HEAD")       # Puntero a la versión actual

def leer_json(ruta, valor_por_defecto=None):
    """
    Carga un archivo JSON de forma segura.
    :param ruta: Ubicación del archivo en el disco.
    :param valor_por_defecto: Qué devolver si el archivo no existe (ej. lista vacía).
    :return: Los datos convertidos a objeto de Python (diccionario o lista).
    """
    if not os.path.exists(ruta):
        return valor_por_defecto
    with open(ruta, 'r') as f:
        return json.load(f)

def escribir_json(ruta, datos):
    """
    Guarda un objeto de Python en formato JSON con indentación para que sea legible.
    :param ruta: Destino del archivo.
    :param datos: Lista o diccionario a guardar.
    """
    with open(ruta, 'w') as f:
        json.dump(datos, f, indent=4)

def leer_texto(ruta):
    """Lee un archivo de texto simple, útil para leer el ID de la versión en HEAD."""
    if not os.path.exists(ruta):
        return ""
    with open(ruta, 'r') as f:
        return f.read().strip()

def escribir_texto(ruta, texto):
    """Escribe una cadena de texto en un archivo, útil para actualizar el puntero HEAD."""
    with open(ruta, 'w') as f:
        f.write(texto)

def generar_id_version():
    """
    Crea un identificador único basado en el Timestamp actual. 
    Esto garantiza que dos versiones no tengan el mismo nombre.
    """
    return "v" + str(int(time.time() * 1000))

def obtener_fecha_actual():
    """Retorna la fecha y hora actual en formato legible (YYYY-MM-DD HH:MM:SS)."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")