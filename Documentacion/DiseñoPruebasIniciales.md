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


| ID | Título / Descripción | Condiciones Previas | Entradas | Pasos de Ejecución | Resultados Esperados | Resultados Reales | Estado |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **GR-01** | Inicializar repositorio vacío | Directorio sin `.sbac` | Ninguno | 1. `sbac init` | Mensaje: "Repositorio SBAC inicializado correctamente". Se crean carpetas ocultas. | | |
| **GR-02** | Doble inicialización | Directorio con `.sbac` existente | Ninguno | 1. `sbac init` | Mensaje: "El repositorio ya está inicializado." | | |
| **GR-03** | Estado sin cambios | Repo inicializado, sin archivos añadidos | Ninguno | 1. `sbac status` | Mensaje: "No hay archivos nuevos pendientes de commit." | | |
| **GR-04** | Estado con archivos en index | Repo inicializado, archivo en index | `file1.txt` | 1. `sbac add file1.txt`<br>2. `sbac status` | El archivo se muestra como `[Pendiente] file1.txt` | | |
| **GR-05** | Historial inicial vacío | Repo sin commits | Ninguno | 1. `sbac history` | Mensaje: "Aún no se han realizado confirmaciones (commits)." | | |
| **GR-06** | Consulta de ayuda principal | CLI instalada | Ninguno | 1. `sbac --help` | Despliega lista de comandos y sintaxis. | | |
| **CV-01** | Agregar archivo individual | Archivo existe localmente | `file.txt` | 1. `sbac add file.txt` | Mensaje: "'file.txt' añadido al seguimiento." | | |
| **CV-02** | Agregar archivo ya rastreado | Archivo ya está en el index | `file.txt` | 1. `sbac add file.txt`<br>2. `sbac add file.txt` | Mensaje: "El archivo ya está siendo rastreado." | | |
| **CV-03** | Intentar agregar directorio | Directorio `src/` existe | `src/` | 1. `sbac add src/` | Error: "El seguimiento de directorios completos no está soportado en esta versión." | | |
| **CV-04** | Commit exitoso (Happy Path) | Archivos en el index | `-m "Fix"` | 1. `sbac commit "Fix"` | Mensaje de éxito con ID del commit. Index se vacía. | | |
| **CV-05** | Commit sin archivos en index | Index vacío | `-m "Vacio"`| 1. `sbac commit "Vacio"` | Mensaje: "Nada para confirmar. Usa 'sbac add'..." | | |
| **CV-06** | Ver historial tras commits | Historial con datos | Ninguno | 1. `sbac history` | Lista de commits cronológica con IDs y mensajes. | | |
| **CV-07** | Colisión de nombres en commit | Archivos homónimos en subcarpetas | `a/f.txt`, `b/f.txt` | 1. `sbac add a/f.txt`<br>2. `sbac add b/f.txt`<br>3. `sbac commit "Test"` | **Fallo esperado (Bug Arquitectónico):** Solo se guarda uno de los `f.txt` en la carpeta del commit. | | |
| **LB-01** | Crear línea base exitosa | Commit en HEAD | `v1.0` | 1. `sbac baseline v1.0` | Mensaje: "Línea base 'v1.0' vinculada..." | | |
| **LB-02** | Crear baseline sin commits | Repositorio vacío | `v1.0` | 1. `sbac baseline v1.0` | Error: "No puedes definir una línea base porque no se ha creado ningún commit..." | | |
| **LB-03** | Checkout a commit exitoso | Commit ID válido en historial | `<ID>` | 1. `sbac checkout <ID>` | Archivos se restauran a su estado. Mensaje de éxito. | | |
| **LB-04** | Checkout a línea base | Línea base `v1.0` válida | `v1.0` | 1. `sbac checkout v1.0` | Archivos se restauran al commit apuntado por la baseline. | | |
| **CP-01** | Diff entre dos commits válidos | 2 commits existentes | `<ID1> <ID2>` | 1. `sbac diff <ID1> <ID2>` | Imprime diferencias (+/-) de los archivos comunes. | | |
| **CP-02** | Diff con versión inexistente | ID erróneo | `ID1 fake_id` | 1. `sbac diff ID1 fake_id` | Error: "Uno o ambos identificadores de versión no existen..." | | |
| **CP-03** | Diff sin archivos comunes | Commits con archivos distintos | `<ID1> <ID2>` | 1. `sbac diff <ID1> <ID2>` | Mensaje: "No se encontraron archivos comunes entre ambas versiones para comparar." | | |
| **CP-04** | Diff de archivos sin cambios | Commits idénticos | `<ID1> <ID1>` | 1. `sbac diff <ID1> <ID1>` | Mensaje indicando que el archivo no presenta cambios. | | |
| **CP-05** | Listar baselines vacío | Sin baselines | Ninguno | 1. `sbac list-baselines`| Mensaje: "No se han registrado líneas base en este repositorio." | | |
| **ME-01** | Ejecutar status sin init | No hay `.sbac` | Ninguno | 1. `sbac status` | Error: "El repositorio SBAC no está inicializado..." | | |
| **ME-02** | Agregar archivo inexistente | Archivo no existe | `fake.py` | 1. `sbac add fake.py` | Error: "El archivo 'fake.py' no existe." | | |
| **ME-03** | Checkout inexistente | Referencia inválida | `fake_tag` | 1. `sbac checkout fake_tag`| Error: "La versión o línea base 'fake_tag' no existe." | | |
| **ME-04** | Commit sin mensaje | Faltan argumentos CLI | Ninguno | 1. `sbac commit` | Error del `argparse`: Falta el argumento de mensaje. | | |
| **ME-05** | Diff de un solo argumento | Falta un argumento CLI | `v1.0` | 1. `sbac diff v1.0` | Error del `argparse`: the following arguments are required. | | |


---
