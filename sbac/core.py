import os
import shutil
import difflib
import utils
import sys
import json

def validar_repositorio(func):
    """Decorador para asegurar que el repositorio esté inicializado antes de operar."""
    def wrapper(*args, **kwargs):
        if not os.path.exists(utils.SBAC_DIR):
            print("Error: El repositorio SBAC no está inicializado. Ejecuta primero 'sbac init'.")
            sys.exit(1) # Ahora sí lanza un error al sistema operativo (INC-004)
        return func(*args, **kwargs)
    return wrapper

def inicializar_repositorio():
    """Crea la estructura de carpetas necesaria para que el sistema funcione."""
    if os.path.exists(utils.SBAC_DIR):
        print("El repositorio ya está inicializado.")
        return
    
    os.makedirs(utils.COMMITS_DIR)
    utils.escribir_json(utils.INDEX_FILE, [])    # Index vacío
    utils.escribir_json(utils.BASELINES_FILE, {}) # Sin líneas base
    utils.escribir_texto(utils.HEAD_FILE, "")     # Sin versiones aún
    print("Repositorio SBAC inicializado correctamente.")

@validar_repositorio
def anadir_archivo(archivo):
    """Añade un archivo al área de seguimiento (Staging Area)."""
    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' no existe.")
        return
    if os.path.isdir(archivo):
        print("Error: El seguimiento de directorios completos no está soportado en esta versión.")
        return
    
    index = utils.leer_json(utils.INDEX_FILE, [])
    if archivo not in index:
        index.append(archivo)
        utils.escribir_json(utils.INDEX_FILE, index)
        print(f"'{archivo}' añadido al seguimiento.")
    else:
        print("El archivo ya está siendo rastreado.")

@validar_repositorio
def mostrar_estado():
    """Compara los archivos en disco con el Index y el último commit para dar un estado real."""
    index = utils.leer_json(utils.INDEX_FILE, [])
    
    archivos_en_head = []
    head_commit = utils.leer_texto(utils.HEAD_FILE)
    
    if head_commit:
        ruta_commit = os.path.join(utils.COMMITS_DIR, head_commit)
        if os.path.exists(ruta_commit):
            for raiz, dirs, archivos in os.walk(ruta_commit):
                for archivo in archivos:
                    # Obtenemos la ruta relativa interna del archivo en el commit
                    ruta_completa = os.path.join(raiz, archivo)
                    ruta_relativa = os.path.relpath(ruta_completa, ruta_commit).replace("\\", "/")
                    # Evitamos meter archivos de control internos si los hubiera
                    archivos_en_head.append(ruta_relativa)

    archivos_en_disco = []
    for raiz, dirs, archivos in os.walk("."):
        if ".sbac" in raiz or "__pycache__" in raiz or ".git" in raiz:
            continue
        for archivo in archivos:
            ruta_completa = os.path.join(raiz, archivo)
            ruta_relativa = os.path.relpath(ruta_completa, ".").replace("\\", "/")
            archivos_en_disco.append(ruta_relativa)

    no_rastreados = []
    for f in archivos_en_disco:
        if f in ["sbac.py", "core.py", "utils.py", "Dockerfile", "test_sbac.py"]:
            continue
        if f not in index and f not in archivos_en_head:
            no_rastreados.append(f)

    if head_commit:
        print(f"Versión actual (HEAD): {head_commit}")
    else:
        print("Versión actual: Ninguna (Repositorio inicializado)")
    print("==============================")

    if index:
        print("Archivos listos para el próximo commit (Staging):")
        for file in index:
            print(f"  [+] {file}")
    else:
        print("No hay cambios guardados.")
        print("  (Usa 'python sbac.py add <archivo>' para agregarlos)")
        
    print("==============================")

    if no_rastreados:
        print("Archivos no rastreados (Untracked files):")
        print("  (No se incluirán en el commit a menos que uses 'sbac add')")
        for file in no_rastreados:
            print(f"  [-] {file}")
    else:
        print("No hay archivos nuevos sin rastrear.")
        
    print("==============================")

@validar_repositorio
def crear_commit(mensaje):
    """Crea una versión permanente de los archivos en el index."""
    index = utils.leer_json(utils.INDEX_FILE, [])
    if not index:
        print("Nada para confirmar. Usa 'sbac add' para añadir archivos.")
        return
    
    commit_id = utils.generar_id_version()
    commit_path = os.path.join(utils.COMMITS_DIR, commit_id)
    os.makedirs(commit_path)
    
    # Guardamos los archivos rastreados mapeando su ruta original y su nombre
    archivos_guardados = {}

    # Heredar archivos del commit anterior (INC-006)
    head_anterior = utils.leer_texto(utils.HEAD_FILE)
    if head_anterior:
        meta_anterior = utils.leer_json(os.path.join(utils.COMMITS_DIR, head_anterior, "meta.json"), {})
        for nombre_base, ruta_orig in meta_anterior.get("archivos", {}).items():
            origen_viejo = os.path.join(utils.COMMITS_DIR, head_anterior, nombre_base)
            dest_nuevo = os.path.join(commit_path, nombre_base)
            if os.path.exists(origen_viejo):
                shutil.copy(origen_viejo, dest_nuevo)
                archivos_guardados[nombre_base] = ruta_orig


    for file in index:
        nombre_base = file.replace("/", "_").replace("\\", "_")
        dest = os.path.join(commit_path, nombre_base)
        shutil.copy(file, dest)
        archivos_guardados[nombre_base] = file # Mantenemos la ruta original de rescate
        
    metadata = {
        "id": commit_id,
        "mensaje": mensaje,
        "fecha": utils.obtener_fecha_actual(),
        "archivos": archivos_guardados
    }
    utils.escribir_json(os.path.join(commit_path, "meta.json"), metadata)
    
    utils.escribir_json(utils.INDEX_FILE, [])
    utils.escribir_texto(utils.HEAD_FILE, commit_id)
    print(f"Versión {commit_id} creada exitosamente.")

def _resolver_identificador(identificador):
    """Función interna para verificar si un ID es un commit directo o una línea base."""
    baselines = utils.leer_json(utils.BASELINES_FILE, {})
    if identificador in baselines:
        return baselines[identificador]
    return identificador

@validar_repositorio
def ver_diferencias(v1, v2):
    """Compara archivos comunes entre dos identificadores (Commit ID o Baseline)."""
    id1 = _resolver_identificador(v1)
    id2 = _resolver_identificador(v2)

    path1 = os.path.join(utils.COMMITS_DIR, id1)
    path2 = os.path.join(utils.COMMITS_DIR, id2)
    
    if not os.path.exists(path1) or not os.path.exists(path2):
        print(f"Error: Uno o ambos identificadores de versión no existen ({v1}, {v2}).")
        return
    
    m1 = utils.leer_json(os.path.join(path1, "meta.json"))
    m2 = utils.leer_json(os.path.join(path2, "meta.json"))
    
    # Detectar añadidos y eliminados (INC-003)
    archivos1 = set(m1['archivos'].keys())
    archivos2 = set(m2['archivos'].keys())

    eliminados = archivos1 - archivos2
    añadidos = archivos2 - archivos1

    for f in eliminados:
        print(f"[-] Eliminado en la segunda versión: {m1['archivos'][f]}")
    for f in añadidos:
        print(f"[+] Añadido en la segunda versión: {m2['archivos'][f]}")
    
    comunes = set(m1['archivos'].keys()).intersection(set(m2['archivos'].keys()))
    
    if not comunes:
        print("No se encontraron archivos comunes entre ambas versiones para comparar.")
        return

    for archivo in comunes:
        f1 = os.path.join(path1, archivo)
        f2 = os.path.join(path2, archivo)
        
        with open(f1, 'r', errors='ignore') as file1, open(f2, 'r', errors='ignore') as file2:
            diff = difflib.unified_diff(
                file1.readlines(), file2.readlines(),
                fromfile=f"{v1}/{archivo}", tofile=f"{v2}/{archivo}"
            )
            lineas = list(diff)
            if lineas:
                for linea in lineas:
                    print(linea, end='')
            else:
                print(f"El archivo '{archivo}' no presenta cambios entre estas versiones.")


@validar_repositorio
def mostrar_historial():
    """[sbac history] Recorre y despliega cronológicamente los metadatos de los commits."""
    if not os.path.exists(utils.COMMITS_DIR):
        print("No hay historial disponible.")
        return

    commits = os.listdir(utils.COMMITS_DIR)
    if not commits:
        print("Aún no se han realizado confirmaciones (commits).")
        return

    # Recopilamos la información de cada meta.json
    historial = []
    for commit_id in commits:
        meta_path = os.path.join(utils.COMMITS_DIR, commit_id, "meta.json")
        if os.path.exists(meta_path):
            meta_data = utils.read_json(meta_path) if hasattr(utils, 'read_json') else utils.leer_json(meta_path)
            historial.append(meta_data)

    # Ordenar por fecha cronológica (los más recientes primero)
    historial.sort(key=lambda x: x['fecha'], reverse=True)

    print("=== HISTORIAL DE VERSIONES ===")
    for c in historial:
        print(f"\nVersión ID: {c['id']}")
        print(f"Fecha:      {c['fecha']}")
        print(f"Mensaje:    {c['mensaje']}")
        print(f"Archivos:   {', '.join(c['archivos'].keys())}")
    print("\n==============================")

@validar_repositorio
def restaurar_version(version_target):
    """[sbac checkout] Reemplaza los archivos del espacio de trabajo con los de la versión elegida."""
    commit_id = _resolver_identificador(version_target)
    commit_path = os.path.join(utils.COMMITS_DIR, commit_id)

    if not os.path.exists(commit_path):
        print(f"Error: La versión o línea base '{version_target}' no existe.")
        return

    meta = utils.leer_json(os.path.join(commit_path, "meta.json"))

    # Limpiar el espacio de trabajo actual (INC-005)
    head_actual = utils.leer_texto(utils.HEAD_FILE)
    if head_actual:
        meta_actual = utils.leer_json(os.path.join(utils.COMMITS_DIR, head_actual, "meta.json"), {})
        for ruta_actual in meta_actual.get("archivos", {}).values():
            if os.path.exists(ruta_actual):
                os.remove(ruta_actual)
    
    # Restaurar cada archivo guardado a su ubicación original de trabajo
    for nombre_base, ruta_original in meta['archivos'].items():
        origen = os.path.join(commit_path, nombre_base)
        
        # Si la ruta original involucraba carpetas previas, asegurar que existan
        dir_destino = os.path.dirname(ruta_original)
        if dir_destino and not os.path.exists(dir_destino):
            os.makedirs(dir_destino)

        shutil.copy(origen, ruta_original)
        print(f"Restaurado: {ruta_original}")

    # Actualizar el puntero HEAD para indicar en qué versión se encuentra el entorno
    utils.escribir_texto(utils.HEAD_FILE, commit_id)
    print(f"\nEspacio de trabajo cambiado exitosamente a '{version_target}' ({commit_id}).")

@validar_repositorio
def crear_linea_base(nombre_linea_base):
    """[sbac baseline] Vincula el commit actual en HEAD a una etiqueta o Baseline."""
    head_commit = utils.leer_texto(utils.HEAD_FILE)
    
    if not head_commit:
        print("Error: No puedes definir una línea base porque no se ha creado ningún commit en el repositorio.")
        return

    baselines = utils.leer_json(utils.BASELINES_FILE, {})
    baselines[nombre_linea_base] = head_commit
    utils.escribir_json(utils.BASELINES_FILE, baselines)
    
    print(f"Línea base '{nombre_linea_base}' vinculada exitosamente al commit {head_commit}.")

@validar_repositorio
def listar_lineas_base():
    """[sbac list-baselines] Despliega las líneas base guardadas en el sistema."""
    baselines = utils.leer_json(utils.BASELINES_FILE, {})
    
    if not baselines:
        print("No se han registrado líneas base en este repositorio.")
        return

    print("=== LÍNEAS BASE DISPONIBLES ===")
    for nombre, commit_id in baselines.items():
        print(f"  • [{nombre}] -> Apunta a la versión: {commit_id}")
    print("===============================")