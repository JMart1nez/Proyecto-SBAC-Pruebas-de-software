# Especificación de Diseño de Pruebas - IEEE 829

## Enfoque de Diseño de Pruebas
Para el diseño sistemático y eficiente de los casos de prueba del CLI SBAC, se aplicaron metodologías formales de pruebas funcionales (Caja Negra) orientadas a maximizar la detección de defectos con el menor número de pruebas posibles:

1. **Partición de Equivalencia (Equivalence Partitioning):** Los dominios de entrada de los diferentes comandos se dividieron en clases válidas (ej. rutas de archivos correctas, identificadores de commits existentes) y clases no válidas (ej. directorios ajenos al repo, comandos sin los flags requeridos). Se asume que probar un valor representativo de cada partición cubre el comportamiento para todo el conjunto.
2. **Análisis de Valores Límite (Boundary Value Analysis):** Se implementó de manera complementaria para evaluar los límites de los datos de entrada y el manejo de memoria en Python. Se aplica particularmente para probar argumentos de la CLI, como:
   * **Límites de texto:** Ingreso de mensajes de commit (`-m`) vacíos, estándar y en el límite máximo de caracteres admitido (ej. 255 o 500 caracteres).
   * **Límites de lotes:** Ejecutar el comando `sbac add` sin argumentos, con un (1) argumento, y con un límite máximo (ej. agregando `.` en un directorio con cientos de archivos).

---

# Especificación de Casos de Prueba (Test Case Specification)

A continuación, se detallan los 27 Casos de Prueba requeridos, organizados en sus 5 áreas funcionales principales.

| ID | Título / Descripción | Condiciones Previas | Datos de Entrada | Pasos de Ejecución | Resultados Esperados | Resultados Reales | Estado |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **GR-01** | Inicialización exitosa de repositorio vacío | Directorio vacío sin estructura SBAC previa | Ninguno | 1. Ejecutar `sbac init` | Se crea estructura interna oculta y se muestra msj de éxito | | |
| **GR-02** | Doble inicialización de repositorio | Directorio ya posee un repositorio SBAC válido | Ninguno | 1. Ejecutar `sbac init` | Error o advertencia de repositorio existente. No corrompe datos actuales | | |
| **GR-03** | Visualización de estado sin cambios | Repositorio recién inicializado, sin archivos | Ninguno | 1. Ejecutar `sbac status` | Mensaje indicando directorio limpio / sin cambios | | |
| **GR-04** | Visualización de estado con no rastreados | Repo inicializado, 1 archivo nuevo en directorio | Archivo `file1.txt` | 1. Crear archivo<br>2. Ejecutar `sbac status` | Archivo listado en sección de "Archivos no rastreados" | | |
| **GR-05** | Visualización de historial inicial | Repositorio sin commits realizados | Ninguno | 1. Ejecutar `sbac history` | Mensaje indicando que el historial está vacío | | |
| **GR-06** | Consulta de ayuda principal | Sistema con CLI SBAC instalado | Ninguno | 1. Ejecutar `sbac --help` | Lista detallada de comandos, sintaxis y uso | | |
| **CV-01** | Agregar archivo individual válido | Repo con archivo nuevo | `f1.txt` | 1. Ejecutar `sbac add f1.txt` | Archivo pasa exitosamente al área de preparación (index) | | |
| **CV-02** | Agregar múltiples archivos simultáneamente | Repo con varios archivos nuevos/modificados | `f1.txt`, `f2.txt` | 1. Ejecutar `sbac add f1.txt f2.txt` | Todos los archivos indicados se agregan al index | | |
| **CV-03** | Agregar todos los archivos del directorio | Archivos en estado untracked/modificados | `.` (Punto) | 1. Ejecutar `sbac add .` | Todo archivo no ignorado se agrega al index masivamente | | |
| **CV-04** | Confirmar cambios con mensaje estándar | Archivos preparados en el index | `-m "Inicial"` | 1. Ejecutar `sbac commit -m "Inicial"` | Commit creado con ID único. Se limpia el index | | |
| **CV-05** | Confirmar cambios con msj largo (Límite) | Archivos preparados en el index | Cadena de texto > 255 caracteres | 1. Ejecutar `sbac commit -m "[TEXTO_LARGO]"` | El sistema acepta el límite máximo sin fallar o truncando | | |
| **CV-06** | Ver historial tras múltiples commits | Repo con 2 o más commits históricos | Ninguno | 1. Ejecutar `sbac history` | Lista ordenada cronológicamente de commits con su ID y mensaje | | |
| **CV-07** | Estado post-modificación de archivo | Archivo previamente rastreado es alterado | Archivo modificado | 1. Modificar archivo<br>2. Ejecutar `sbac status` | Archivo se lista en "Cambios no preparados para confirmación" | | |
| **LB-01** | Crear una línea base exitosa | Repo con historial de commits válido | `v1.0` | 1. Ejecutar `sbac baseline v1.0` | Etiqueta `v1.0` se crea apuntando al último commit (HEAD) | | |
| **LB-02** | Crear línea base con nombre duplicado | Línea base `v1.0` ya existe | `v1.0` | 1. Ejecutar `sbac baseline v1.0` | Error indicando que el nombre ya está en uso. No se sobrescribe | | |
| **LB-03** | Restaurar a un commit previo exitoso | Historial con múltiples commits | `<ID_COMMIT>` | 1. Ejecutar `sbac checkout <ID_COMMIT>` | Los archivos locales se revierten al estado exacto del commit indicado | | |
| **LB-04** | Restaurar código a línea base existente | Línea base `v1.0` previamente creada | `v1.0` | 1. Ejecutar `sbac checkout v1.0` | Los archivos locales se revierten al estado de la baseline indicada | | |
| **CP-01** | Comparar directorio local vs index | Archivo rastreado fue modificado localmente | Ninguno | 1. Ejecutar `sbac diff` | Imprime diferencias (+/-) del archivo frente a su copia en el index | | |
| **CP-02** | Comparar directorio local vs último commit | Archivo modificado localmente | `HEAD` | 1. Ejecutar `sbac diff HEAD` | Imprime diferencias entre versión local y último snapshot (HEAD) | | |
| **CP-03** | Comparar entre dos commits específicos | Existen al menos 2 commits en historial | `<ID_1>`, `<ID_2>` | 1. Ejecutar `sbac diff <ID_1> <ID_2>` | Imprime diferencias consolidadas entre ambos snapshots | | |
| **CP-04** | Comparar cuando no hay cambios | Directorio completamente limpio | Ninguno | 1. Ejecutar `sbac diff` | No muestra salida, o muestra mensaje "No hay diferencias" | | |
| **CP-05** | Comparar con archivo no rastreado | Archivo nuevo untracked presente | Ninguno | 1. Ejecutar `sbac diff` | Archivo nuevo se ignora, no hay volcado de contenido difuso | | |
| **ME-01** | Comando en directorio no inicializado | Directorio sin estructura SBAC oculta | Ninguno | 1. Ejecutar `sbac status` | Error fatal: "El directorio actual no es un repositorio SBAC" | | |
| **ME-02** | Intentar agregar archivo inexistente | Repo inicializado correctamente | `fake.txt` | 1. Ejecutar `sbac add fake.txt` | Error: "Archivo o directorio no encontrado". Index no se altera | | |
| **ME-03** | Commit con omisión de argumentos obligatorios | Cambios preparados en index | Ninguno | 1. Ejecutar `sbac commit` | Error de sintaxis: Falta el argumento de mensaje (`-m`) | | |
| **ME-04** | Checkout hacia referencia inexistente | Repo inicializado | `tag_invalido` | 1. Ejecutar `sbac checkout tag_invalido` | Error: "Referencia de commit o línea base no encontrada" | | |
| **ME-05** | Ejecución sobre repositorio corrupto | Directorio interno crítico de SBAC borrado | Ninguno | 1. Eliminar dir interno.<br>2. Ejecutar `sbac status` | El sistema captura la excepción y avisa de repositorio corrupto | | |

---
