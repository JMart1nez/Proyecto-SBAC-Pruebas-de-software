import argparse
import core

def main():
    """
    Punto de entrada de la aplicación.
    Configura todos los comandos que el usuario puede escribir en la terminal.
    """
    parser = argparse.ArgumentParser(description="SBAC - Sistema Básico de Administración de Configuración")
    
    # Contenedor de subcomandos
    subparsers = parser.add_subparsers(dest="comando", help="Acción a realizar")

    # Definición de 'init'
    subparsers.add_parser("init", help="Inicializa el repositorio de configuración")

    # Definición de 'add'
    p_add = subparsers.add_parser("add", help="Añade un archivo al área de seguimiento")
    p_add.add_argument("archivo", help="Nombre o ruta del archivo")

    # Definición de 'commit'
    p_commit = subparsers.add_parser("commit", help="Guarda una nueva versión")
    p_commit.add_argument("mensaje", help="Descripción de los cambios realizados")

    # Definición de 'diff' (Modificado para aceptar tanto IDs como nombres de líneas base)
    p_diff = subparsers.add_parser("diff", help="Compara dos versiones o líneas base")
    p_diff.add_argument("v1", help="ID de la versión inicial o nombre de línea base")
    p_diff.add_argument("v2", help="ID de la versión final o nombre de línea base")

    # Definición de 'status'
    subparsers.add_parser("status", help="Muestra el estado de los archivos")
    
    # Definición de 'history'
    subparsers.add_parser("history", help="Muestra el historial cronológico de versiones")

    # Definición de 'checkout'
    p_checkout = subparsers.add_parser("checkout", help="Regresa el espacio de trabajo a una versión específica")
    p_checkout.add_argument("version", help="ID de la versión o nombre de línea base a la que regresar")

    # Definición de 'baseline'
    p_baseline = subparsers.add_parser("baseline", help="Asocia una etiqueta de línea base a la versión actual (HEAD)")
    p_baseline.add_argument("nombre", help="Nombre descriptivo para la línea base")

    # Definición de 'list-baselines'
    subparsers.add_parser("list-baselines", help="Lista todas las líneas base creadas")

    # PROCESAMIENTO: Leemos lo que el usuario escribió
    args = parser.parse_args()

    # Mapeo de comandos a funciones del CORE
    if args.comando == "init":
        core.inicializar_repositorio()
    elif args.comando == "add":
        core.anadir_archivo(args.archivo)
    elif args.comando == "status":
        core.mostrar_estado()
    elif args.comando == "commit":
        core.crear_commit(args.mensaje)
    elif args.comando == "diff":
        core.ver_diferencias(args.v1, args.v2)
    elif args.comando == "history":
        core.mostrar_historial()
    elif args.comando == "checkout":
        core.restaurar_version(args.version)
    elif args.comando == "baseline":
        core.crear_linea_base(args.nombre)
    elif args.comando == "list-baselines":
        core.listar_lineas_base()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()