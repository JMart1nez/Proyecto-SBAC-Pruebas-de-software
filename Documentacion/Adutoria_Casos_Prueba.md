# Primer Informe de Auditoría y Especificación de Casos de Prueba (IEEE 829)

**Proyecto:** Sistema Básico de Administración de Configuración (SBAC)

## 1. Auditoría del Código

He analizado exhaustivamente la lógica del backend implementada en `core.py` y el enrutador de comandos en `sbac.py`.

### 1.1 Inconsistencias Críticas y Riesgos de Configuración

He detectado divergencias graves entre el diseño conceptual y la implementación técnica. Estos hallazgos representan **Riesgos de Configuración Críticos**:

> [!WARNING]
> **Riesgo 1: Soporte de Directorios en `sbac add` (Brecha de Trazabilidad)**
> *   *Diseño:* El plan original (CV-03) estipulaba que `sbac add .` agregaría todos los archivos del directorio.
> *   *Código:* La función `anadir_archivo(archivo)` en `core.py` lanza un error explícito: `"Error: El seguimiento de directorios completos no está soportado en esta versión."`. Existe una desconexión total entre lo requerido y lo programado.

> [!CAUTION]
> **Riesgo 2: Colisión de Nombres en el Staging Area (Fallo Arquitectónico)**
> *   *Código:* En `crear_commit`, los archivos se guardan usando únicamente su nombre base (`nombre_base = os.path.basename(file)`). Si un usuario añade `src/main.py` y `test/main.py`, el sistema sobrescribirá el primero con el segundo dentro de la carpeta del commit (`dest = os.path.join(commit_path, nombre_base)`). Esto provocará **pérdida de datos silenciosa e irreversible**.

> [!IMPORTANT]
> **Riesgo 3: Restauración Parcial en `sbac checkout` (Estado Sucio)**
> *   *Código (P2):* La función `restaurar_version` copia los archivos del commit objetivo de vuelta a su `ruta_original`. Sin embargo, no elimina los archivos que el usuario haya creado *después* de ese commit. Esto deja el espacio de trabajo en un "estado sucio" (mezcla de archivos del commit antiguo y archivos nuevos no trackeados).
