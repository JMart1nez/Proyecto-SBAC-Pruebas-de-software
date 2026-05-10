import argparse
import core

def main():
    """
    Punto de entrada de la aplicación.
    Configura todos los comandos que el usuario puede escribir en la terminal.
    """
    parser = argparse.ArgumentParser(description="SBAC - Sistema Básico de Administración de Configuración")
    
    # Creamos un contenedor de subcomandos (init, add, commit, etc.)
    subparsers = parser.add_subparsers(dest="comando", help="Acción a realizar")

    # Definición de 'init'
    subparsers.add_parser("init", help="Inicializa el repositorio de configuración")

    # Definición de 'add' (requiere un argumento: el nombre del archivo)
    p_add = subparsers.add_parser("add", help="Añade un archivo al área de seguimiento")
    p_add.add_argument("archivo", help="Nombre o ruta del archivo")

    # Definición de 'commit' (requiere un mensaje descriptivo)
    p_commit = subparsers.add_parser("commit", help="Guarda una nueva versión")
    p_commit.add_argument("mensaje", help="Descripción de los cambios realizados")

    # Definición de 'diff' (requiere dos IDs de versión para comparar)
    p_diff = subparsers.add_parser("diff", help="Compara dos versiones")
    p_diff.add_argument("v1", help="ID de la versión inicial")
    p_diff.add_argument("v2", help="ID de la versión final")

    # Definición de 'status'
    subparsers.add_parser("status", help="Muestra el estado de los archivos")

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
    else:
        # Si no escribe nada o escribe algo mal, mostramos la ayuda
        parser.print_help()

if __name__ == "__main__":
    main()