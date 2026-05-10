import os
import shutil
import difflib
import utils

def inicializar_repositorio():
    """Crea la estructura de carpetas necesaria para que el sistema funcione."""
    if os.path.exists(utils.SBAC_DIR):
        print("El repositorio ya está inicializado.")
        return
    
    # Creamos las carpetas y los archivos de metadatos iniciales
    os.makedirs(utils.COMMITS_DIR)
    utils.escribir_json(utils.INDEX_FILE, [])    # Index vacío
    utils.escribir_json(utils.BASELINES_FILE, {}) # Sin líneas base
    utils.escribir_texto(utils.HEAD_FILE, "")     # Sin versiones aún
    print("Repositorio SBAC inicializado correctamente.")

def anadir_archivo(archivo):
    """Añade un archivo al 'área de preparación' (Staging Area)."""
    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' no existe.")
        return
    
    # Leemos la lista actual, añadimos el nuevo y guardamos
    index = utils.leer_json(utils.INDEX_FILE, [])
    if archivo not in index:
        index.append(archivo)
        utils.escribir_json(utils.INDEX_FILE, index)
        print(f"'{archivo}' añadido al seguimiento.")
    else:
        print("El archivo ya está siendo rastreado.")

def mostrar_estado():
    """Compara qué archivos están en el index listos para guardarse."""
    index = utils.leer_json(utils.INDEX_FILE, [])
    print("Estado actual del repositorio:")
    if not index:
        print("  No hay archivos nuevos pendientes de commit.")
    for file in index:
        print(f"  [Pendiente] {file}")

def crear_commit(mensaje):
    """
    Crea una versión permanente de los archivos en el index.
    Copia los archivos físicamente a una carpeta nueva y genera metadatos JSON.
    """
    index = utils.leer_json(utils.INDEX_FILE, [])
    if not index:
        print("Nada para confirmar. Usa 'sbac add'.")
        return
    
    # 1. Preparar la nueva carpeta de versión
    commit_id = utils.generar_id_version()
    commit_path = os.path.join(utils.COMMITS_DIR, commit_id)
    os.makedirs(commit_path)
    
    # 2. Copiar archivos del usuario a la carpeta de la versión
    for file in index:
        dest = os.path.join(commit_path, os.path.basename(file))
        shutil.copy(file, dest)
        
    # 3. Guardar metadatos (quién, qué y cuándo)
    metadata = {
        "id": commit_id,
        "mensaje": mensaje,
        "fecha": utils.obtener_fecha_actual(),
        "archivos": [os.path.basename(f) for f in index]
    }
    utils.escribir_json(os.path.join(commit_path, "meta.json"), metadata)
    
    # 4. Limpiar index y actualizar el puntero HEAD
    utils.escribir_json(utils.INDEX_FILE, [])
    utils.escribir_texto(utils.HEAD_FILE, commit_id)
    print(f"Versión {commit_id} creada exitosamente.")

def ver_diferencias(v1, v2):
    """
    Usa la biblioteca 'difflib' para comparar archivos entre dos versiones.
    Busca archivos que tengan el mismo nombre en ambos commits.
    """
    path1 = os.path.join(utils.COMMITS_DIR, v1)
    path2 = os.path.join(utils.COMMITS_DIR, v2)
    
    # Obtenemos metadatos para saber qué archivos comparar
    m1 = utils.leer_json(os.path.join(path1, "meta.json"))
    m2 = utils.leer_json(os.path.join(path2, "meta.json"))
    
    # Intersección: Solo comparamos archivos que existan en ambos commits
    comunes = set(m1['archivos']).intersection(set(m2['archivos']))
    
    for archivo in comunes:
        f1 = os.path.join(path1, archivo)
        f2 = os.path.join(path2, archivo)
        
        with open(f1, 'r') as file1, open(f2, 'r') as file2:
            # difflib genera el formato 'unified diff' (+ para añadido, - para borrado)
            diff = difflib.unified_diff(
                file1.readlines(), file2.readlines(),
                fromfile=f"v1/{archivo}", tofile=f"v2/{archivo}"
            )
            for linea in diff:
                print(linea, end='')