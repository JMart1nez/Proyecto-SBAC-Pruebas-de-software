# Especificación de Diseño de Pruebas - IEEE 829

## Enfoque de Diseño de Pruebas
Para el diseño sistemático y eficiente de los casos de prueba del CLI SBAC, se aplicaron metodologías formales de pruebas funcionales (Caja Negra) orientadas a maximizar la detección de defectos con el menor número de pruebas posibles:

1. **Partición de Equivalencia (Equivalence Partitioning):** Los dominios de entrada de los diferentes comandos se dividieron en clases válidas (ej. rutas de archivos correctas, identificadores de commits existentes) y clases no válidas (ej. directorios ajenos al repo, comandos sin los flags requeridos). Se asume que probar un valor representativo de cada partición cubre el comportamiento para todo el conjunto.
2. **Análisis de Valores Límite (Boundary Value Analysis):** Se implementó de manera complementaria para evaluar los límites de los datos de entrada y el manejo de memoria en Python. Se aplica particularmente para probar argumentos de la CLI, como:
   * **Límites de texto:** Ingreso de mensajes de commit vacíos, estándar y en el límite máximo de caracteres admitido.
   * **Límites de lotes:** Ejecutar el comando `sbac add` sin argumentos, con un (1) argumento, y con un directorio completo.

---

# Especificación de Casos de Prueba (Test Case Specification)

A continuación, se detallan los 27 Casos de Prueba ejecutados, organizados en sus 5 áreas funcionales principales.

**Fecha de ejecución:** 27 de Mayo de 2026  
**Ejecutado por:** Persona 3 — QA Lead  
**Versión del sistema:** Código actualizado por Diana-Matu — "feat: Se añadieron funciones faltantes"

---

| ID | Título / Descripción | Condiciones Previas | Entradas | Pasos de Ejecución | Resultados Esperados | Resultados Reales | Estado |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **GR-01** | Inicializar repositorio vacío | Directorio sin `.sbac` | Ninguno | 1. `python3 sbac.py init` | Mensaje: "Repositorio SBAC inicializado correctamente". Se crean carpetas ocultas. | `Repositorio SBAC inicializado correctamente.` Carpeta `.sbac/` creada con subcarpetas `commits/`, `index.json`, `baselines.json` y `HEAD`. | ✅ PASS |
| **GR-02** | Doble inicialización | Directorio con `.sbac` existente | Ninguno | 1. `python3 sbac.py init` (segunda vez) | Mensaje: "El repositorio ya está inicializado." | `El repositorio ya está inicializado.` | ✅ PASS |
| **GR-03** | Estado sin cambios | Repo inicializado, sin archivos añadidos | Ninguno | 1. `python3 sbac.py status` | Mensaje: "No hay archivos nuevos pendientes de commit." | `Estado actual del repositorio:` / `No hay archivos nuevos pendientes de commit.` | ✅ PASS |
| **GR-04** | Estado con archivos en index | Repo inicializado, archivo en index | `archivo1.txt` | 1. `python3 sbac.py add archivo1.txt` 2. `python3 sbac.py status` | El archivo se muestra como `[Pendiente] archivo1.txt` | `'archivo1.txt' añadido al seguimiento.` / `Estado actual del repositorio:` / `[Pendiente] archivo1.txt` | ✅ PASS |
| **GR-05** | Historial inicial vacío | Repo sin commits | Ninguno | 1. `python3 sbac.py init` 2. `python3 sbac.py history` | Mensaje: "Aún no se han realizado confirmaciones (commits)." | `Aún no se han realizado confirmaciones (commits).` | ✅ PASS |
| **GR-06** | Consulta de ayuda principal | CLI instalada | Ninguno | 1. `python3 sbac.py --help` | Despliega lista de comandos y sintaxis. | Lista completa con los 9 comandos: `init, add, commit, diff, status, history, checkout, baseline, list-baselines` | ✅ PASS |
| **CV-01** | Agregar archivo individual | Archivo existe localmente | `miarchivo.txt` | 1. `python3 sbac.py add miarchivo.txt` | Mensaje: "'miarchivo.txt' añadido al seguimiento." | `'miarchivo.txt' añadido al seguimiento.` | ✅ PASS |
| **CV-02** | Agregar archivo ya rastreado | Archivo ya está en el index | `miarchivo.txt` | 1. `python3 sbac.py add miarchivo.txt` (segunda vez) | Mensaje: "El archivo ya está siendo rastreado." | `El archivo ya está siendo rastreado.` | ✅ PASS |
| **CV-03** | Intentar agregar directorio | Directorio `carpeta/` existe | `carpeta/` | 1. `python3 sbac.py add carpeta` | Error: "El seguimiento de directorios completos no está soportado en esta versión." | `Error: El seguimiento de directorios completos no está soportado en esta versión.` | ✅ PASS |
| **CV-04** | Commit exitoso (Happy Path) | Archivos en el index | `"Primera versión"` | 1. `python3 sbac.py commit "Primera versión"` | Mensaje de éxito con ID del commit. Index se vacía. | `Versión v1779937671 creada exitosamente.` Index vaciado correctamente. | ✅ PASS |
| **CV-05** | Commit sin archivos en index | Index vacío | `"Sin archivos"` | 1. `python3 sbac.py commit "Sin archivos"` | Mensaje: "Nada para confirmar. Usa 'sbac add'..." | `Nada para confirmar. Usa 'sbac add' para añadir archivos.` | ✅ PASS |
| **CV-06** | Ver historial tras commits | Historial con datos | Ninguno | 1. `python3 sbac.py history` | Lista de commits cronológica con IDs y mensajes. | `=== HISTORIAL DE VERSIONES ===` / `Versión ID: v1779937671` / `Fecha: 2026-05-27 21:07:51` / `Mensaje: Primera versión` / `Archivos: miarchivo.txt` | ✅ PASS |
| **CV-07** | Colisión de nombres en commit | Archivos homónimos en subcarpetas | `src/main.py`, `test/main.py` | 1. `python3 sbac.py add src/main.py` 2. `python3 sbac.py add test/main.py` 3. `python3 sbac.py commit "Colision"` 4. `ls .sbac/commits/vID/` | **Fallo esperado (Bug Arquitectónico):** Solo se guarda uno de los `main.py` en la carpeta del commit. | El sistema reportó `Versión v1779937860 creada exitosamente.` pero `ls .sbac/commits/v1779937860/` solo mostró `main.py meta.json`. El archivo `src/main.py` fue sobrescrito silenciosamente por `test/main.py`. Ver **INC-001**. | ❌ FAIL |
| **LB-01** | Crear línea base exitosa | Commit en HEAD | `v1.0` | 1. `python3 sbac.py baseline v1.0` | Mensaje: "Línea base 'v1.0' vinculada..." | `Línea base 'v1.0' vinculada exitosamente al commit v1779939080.` | ✅ PASS |
| **LB-02** | Crear baseline sin commits | Repositorio vacío | `v1.0` | 1. `python3 sbac.py init` 2. `python3 sbac.py baseline v1.0` | Error: "No puedes definir una línea base porque no se ha creado ningún commit..." | `Error: No puedes definir una línea base porque no se ha creado ningún commit en el repositorio.` | ✅ PASS |
| **LB-03** | Checkout a commit exitoso | Commit ID válido en historial | `v1779939080` | 1. Modificar archivo 2. `python3 sbac.py checkout v1779939080` 3. Verificar contenido | Archivos se restauran a su estado. Mensaje de éxito. | `Restaurado: archivo.txt` / `Espacio de trabajo cambiado exitosamente a 'v1779939080' (v1779939080).` Contenido verificado con `cat`: devolvió `contenido v1`. | ✅ PASS |
| **LB-04** | Checkout a línea base | Línea base `v1.0` válida | `v1.0` | 1. Modificar archivo 2. `python3 sbac.py checkout v1.0` 3. Verificar contenido | Archivos se restauran al commit apuntado por la baseline. | `Restaurado: archivo.txt` / `Espacio de trabajo cambiado exitosamente a 'v1.0' (v1779939080).` Contenido verificado con `cat`: devolvió `contenido v1`. | ✅ PASS |
| **CP-01** | Diff entre dos commits válidos | 2 commits existentes | `v1779939492 v1779939519` | 1. `python3 sbac.py diff v1779939492 v1779939519` | Imprime diferencias (+/-) de los archivos comunes. | `--- v1779939492/archivo.txt` / `+++ v1779939519/archivo.txt` / `@@ -1 +1 @@` / `-linea 1` / `+linea 1 modificada` | ✅ PASS |
| **CP-02** | Diff con versión inexistente | ID erróneo | `v1779939492 id_falso` | 1. `python3 sbac.py diff v1779939492 id_falso` | Error: "Uno o ambos identificadores de versión no existen..." | `Error: Uno o ambos identificadores de versión no existen (v1779939492, id_falso).` | ✅ PASS |
| **CP-03** | Diff sin archivos comunes | Commits con archivos distintos | `v1779939814 v1779939492` | 1. `python3 sbac.py diff v1779939814 v1779939492` | Mensaje: "No se encontraron archivos comunes entre ambas versiones para comparar." | `No se encontraron archivos comunes entre ambas versiones para comparar.` Nota: Durante preparación de este caso se detectó **INC-002** (colisión de timestamps). | ✅ PASS |
| **CP-04** | Diff de archivos sin cambios | Mismo commit comparado consigo mismo | `v1779939492 v1779939492` | 1. `python3 sbac.py diff v1779939492 v1779939492` | Mensaje indicando que el archivo no presenta cambios. | `El archivo 'archivo.txt' no presenta cambios entre estas versiones.` | ✅ PASS |
| **CP-05** | Listar baselines vacío | Sin baselines registradas | Ninguno | 1. `python3 sbac.py list-baselines` | Mensaje: "No se han registrado líneas base en este repositorio." | `No se han registrado líneas base en este repositorio.` | ✅ PASS |
| **ME-01** | Ejecutar status sin init | No hay `.sbac` | Ninguno | 1. `python3 sbac.py status` | Error: "El repositorio SBAC no está inicializado..." | `Error: El repositorio SBAC no está inicializado. Ejecuta primero 'sbac init'.` | ✅ PASS |
| **ME-02** | Agregar archivo inexistente | Archivo no existe | `archivo_fantasma.py` | 1. `python3 sbac.py add archivo_fantasma.py` | Error: "El archivo 'archivo_fantasma.py' no existe." | `Error: El archivo 'archivo_fantasma.py' no existe.` | ✅ PASS |
| **ME-03** | Checkout inexistente | Referencia inválida | `etiqueta_falsa` | 1. `python3 sbac.py checkout etiqueta_falsa` | Error: "La versión o línea base 'etiqueta_falsa' no existe." | `Error: La versión o línea base 'etiqueta_falsa' no existe.` | ✅ PASS |
| **ME-04** | Commit sin mensaje | Faltan argumentos CLI | Ninguno | 1. `python3 sbac.py commit` | Error del `argparse`: Falta el argumento de mensaje. | `usage: sbac.py commit [-h] mensaje` / `sbac.py commit: error: the following arguments are required: mensaje` | ✅ PASS |
| **ME-05** | Diff de un solo argumento | Falta un argumento CLI | `v1.0` | 1. `python3 sbac.py diff v1.0` | Error del `argparse`: the following arguments are required. | `usage: sbac.py diff [-h] v1 v2` / `sbac.py diff: error: the following arguments are required: v2` | ✅ PASS |

---

## Resumen de Ejecución

| Grupo | Total | PASS | FAIL |
|-------|-------|------|------|
| GR — Gestión de Repositorio | 6 | 6 | 0 |
| CV — Control de Versiones | 7 | 5 | 2 |
| LB — Líneas Base | 4 | 4 | 0 |
| CP — Comparación | 5 | 5 | 0 |
| ME — Manejo de Errores | 5 | 5 | 0 |
| **Total** | **27** | **25** | **2** |

**Tasa de éxito: 92.6%**

---

## Defectos Relacionados

| ID Incidente | Caso | Severidad | Descripción breve |
|-------------|------|-----------|-------------------|
| INC-001 | CV-07 | Alta | Colisión de nombres — pérdida silenciosa de archivos en commit |
| INC-002 | CP-03 | Alta | Colisión de timestamps — commits ejecutados en el mismo segundo generan IDs duplicados |

*Ver documento `Reporte_Incidentes.md` para detalle completo de cada defecto.*

---

*Ejecutado por: Persona 3 — QA Lead / Pruebas*  
*Fecha: 27 de Mayo de 2026*
