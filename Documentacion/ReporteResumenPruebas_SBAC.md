# Reporte Resumen de Pruebas — IEEE 829
## Sistema Básico de Administración de Configuración (SBAC)

**Identificador del Documento:** TSR-SBAC-V1.0  
**Proyecto:** Sistema Básico de Administración de Configuración (SBAC)  
**Fecha de ejecución:** 27 de Mayo de 2026  
**Versión del sistema probado:** Código actualizado — commit "feat: Se añadieron funciones faltantes" (Diana-Matu)  
**Responsable de QA:** Belen-Diaz QA Lead / Pruebas  
**Versión del documento:** 1.0  

---

## 1. Introducción

Este documento presenta el reporte final de las actividades de pruebas realizadas sobre el sistema SBAC (Sistema Básico de Administración de Configuración), una herramienta de línea de comandos desarrollada en Python que implementa funciones básicas de control de versiones. El reporte cubre las tres etapas de trabajo del QA Lead: el desarrollo del plan de pruebas (Semana 1), la ejecución de pruebas de integración (Semana 3) y las pruebas completas del sistema (Semana 4).

Las pruebas se ejecutaron directamente en terminal sobre el sistema real, verificando que cada comando del CLI respondiera correctamente tanto en condiciones normales como ante entradas inválidas o situaciones de error.

---

## 2. Alcance de las Pruebas

Se evaluaron las siguientes funcionalidades del sistema:

| Comando | Funcionalidad |
|---------|--------------|
| `sbac init` | Inicialización del repositorio |
| `sbac add` | Añadir archivos al área de seguimiento |
| `sbac status` | Consultar estado del repositorio |
| `sbac commit` | Crear una nueva versión |
| `sbac history` | Ver historial de versiones |
| `sbac baseline` | Crear una línea base |
| `sbac list-baselines` | Listar líneas base disponibles |
| `sbac checkout` | Restaurar una versión anterior |
| `sbac diff` | Comparar diferencias entre versiones |

Las pruebas se organizaron en cinco grupos funcionales con un total de 27 casos de prueba.

---

## 3. Entorno de Pruebas

- **Sistema operativo:** Ubuntu (Linux)
- **Lenguaje:** Python 3
- **Archivos del sistema:** `core.py`, `sbac.py`, `utils.py`
- **Método de ejecución:** Terminal, comandos manuales
- **Directorio de trabajo:** `~/miparte/`
- **Herramienta de comparación:** Biblioteca `difflib` de Python (integrada en el sistema)

---

## 4. Estrategia de Pruebas Aplicada

Se combinaron dos enfoques:

**Pruebas de Caja Negra:** Se ejecutaron los comandos del CLI como lo haría un usuario real, evaluando únicamente las salidas en terminal sin revisar el código interno. Se aplicaron técnicas de partición de equivalencia (entradas válidas vs. inválidas) y análisis de valores límite.

**Pruebas de Integración:** Se verificó que los módulos del sistema (`utils.py`, `core.py`, `sbac.py`) trabajaran correctamente en conjunto, ejecutando flujos completos de múltiples pasos como `init → add → commit → diff`.

---

## 5. Ejecución de Casos de Prueba

### 5.1 Grupo GR — Gestión de Repositorio

Este grupo verifica las funciones básicas de inicialización y consulta de estado del repositorio.

---

**GR-01 — Inicializar repositorio vacío**

```bash
mkdir test_sbac && cd test_sbac
python3 ../sbac.py init
```

Salida esperada:
```
Repositorio SBAC inicializado correctamente.
```

Salida obtenida:
```
Repositorio SBAC inicializado correctamente.
```

**Estado: PASS**

---

**GR-02 — Doble inicialización**

```bash
python3 ../sbac.py init
```
*(ejecutado por segunda vez en el mismo directorio)*

Salida esperada:
```
El repositorio ya está inicializado.
```

Salida obtenida:
```
El repositorio ya está inicializado.
```

**Estado: PASS**

---

**GR-03 — Estado sin archivos añadidos**

```bash
python3 ../sbac.py status
```

Salida esperada:
```
Estado actual del repositorio:
  No hay archivos nuevos pendientes de commit.
```

Salida obtenida:
```
Estado actual del repositorio:
  No hay archivos nuevos pendientes de commit.
```

**Estado: PASS**

---

**GR-04 — Estado con archivo en el index**

```bash
echo "hola" > archivo1.txt
python3 ../sbac.py add archivo1.txt
python3 ../sbac.py status
```

Salida esperada:
```
'archivo1.txt' añadido al seguimiento.
Estado actual del repositorio:
  [Pendiente] archivo1.txt
```

Salida obtenida:
```
'archivo1.txt' añadido al seguimiento.
Estado actual del repositorio:
  [Pendiente] archivo1.txt
```

**Estado: PASS**

---

**GR-05 — Historial inicial vacío**

```bash
mkdir test_gr05 && cd test_gr05
python3 ../sbac.py init
python3 ../sbac.py history
```

Salida esperada:
```
Aún no se han realizado confirmaciones (commits).
```

Salida obtenida:
```
Aún no se han realizado confirmaciones (commits).
```

**Estado: PASS**

---

**GR-06 — Consulta de ayuda principal**

```bash
python3 sbac.py --help
```

Salida esperada: lista de todos los comandos disponibles.

Salida obtenida:
```
usage: sbac.py [-h]
               {init,add,commit,diff,status,history,checkout,baseline,list-baselines}
               ...
SBAC - Sistema Básico de Administración de Configuración
positional arguments:
  {init,add,commit,diff,status,history,checkout,baseline,list-baselines}
    init                Inicializa el repositorio de configuración
    add                 Añade un archivo al área de seguimiento
    commit              Guarda una nueva versión
    diff                Compara dos versiones o líneas base
    status              Muestra el estado de los archivos
    history             Muestra el historial cronológico de versiones
    checkout            Regresa el espacio de trabajo a una versión específica
    baseline            Asocia una etiqueta de línea base a la versión actual
    list-baselines      Lista todas las líneas base creadas
```

**Estado: PASS**

---

### 5.2 Grupo CV — Control de Versiones

Este grupo valida el flujo principal del sistema: añadir archivos, confirmar versiones y consultar el historial. También incluye un caso de prueba que documenta un defecto arquitectónico conocido.

---

**CV-01 — Agregar archivo individual**

```bash
python3 ../sbac.py init
echo "version 1" > miarchivo.txt
python3 ../sbac.py add miarchivo.txt
```

Salida esperada:
```
'miarchivo.txt' añadido al seguimiento.
```

Salida obtenida:
```
'miarchivo.txt' añadido al seguimiento.
```

**Estado: PASS**

---

**CV-02 — Agregar archivo ya rastreado**

```bash
python3 ../sbac.py add miarchivo.txt
```
*(ejecutado por segunda vez)*

Salida esperada:
```
El archivo ya está siendo rastreado.
```

Salida obtenida:
```
El archivo ya está siendo rastreado.
```

**Estado: PASS**

---

**CV-03 — Intentar añadir un directorio**

```bash
mkdir carpeta
python3 ../sbac.py add carpeta
```

Salida esperada:
```
Error: El seguimiento de directorios completos no está soportado en esta versión.
```

Salida obtenida:
```
Error: El seguimiento de directorios completos no está soportado en esta versión.
```

**Estado: PASS**

---

**CV-04 — Commit exitoso (Happy Path)**

```bash
python3 ../sbac.py commit "Primera versión"
```

Salida esperada:
```
Versión vXXXXXXXXXX creada exitosamente.
```

Salida obtenida:
```
Versión v1779937671 creada exitosamente.
```

**Estado: PASS**

---

**CV-05 — Commit sin archivos en el index**

```bash
python3 ../sbac.py commit "Sin archivos"
```

Salida esperada:
```
Nada para confirmar. Usa 'sbac add' para añadir archivos.
```

Salida obtenida:
```
Nada para confirmar. Usa 'sbac add' para añadir archivos.
```

**Estado: PASS**

---

**CV-06 — Ver historial tras commits**

```bash
python3 ../sbac.py history
```

Salida esperada: lista cronológica con ID, fecha, mensaje y archivos del commit.

Salida obtenida:
```
=== HISTORIAL DE VERSIONES ===

Versión ID: v1779937671
Fecha:      2026-05-27 21:07:51
Mensaje:    Primera versión
Archivos:   miarchivo.txt

==============================
```

**Estado: PASS**

---

**CV-07 — Colisión de nombres en commit (Bug Arquitectónico)**

```bash
mkdir -p src test
echo "version a" > src/main.py
echo "version b" > test/main.py
python3 ../sbac.py add src/main.py
python3 ../sbac.py add test/main.py
python3 ../sbac.py commit "Colision de nombres"
ls .sbac/commits/v1779937860/
```

Salida esperada: ambos archivos guardados dentro de la carpeta del commit.

Salida obtenida:
```
'src/main.py' añadido al seguimiento.
'test/main.py' añadido al seguimiento.
Versión v1779937860 creada exitosamente.

main.py  meta.json
```

Solo aparece un `main.py`. El sistema sobrescribió `src/main.py` con `test/main.py` sin advertir al usuario y reportó éxito de forma incorrecta.

**Estado: FAIL  — Ver INC-001**

---

### 5.3 Grupo LB — Líneas Base

Este grupo verifica la creación de líneas base y la restauración de versiones anteriores mediante `checkout`

---

**LB-01 — Crear línea base exitosa**

```bash
python3 ../sbac.py init
echo "contenido v1" > archivo.txt
python3 ../sbac.py add archivo.txt
python3 ../sbac.py commit "Version inicial"
python3 ../sbac.py baseline v1.0
```

Salida esperada:
```
Línea base 'v1.0' vinculada exitosamente al commit vXXXXXXXXXX.
```

Salida obtenida:
```
Línea base 'v1.0' vinculada exitosamente al commit v1779939080.
```

**Estado: PASS **

---

**LB-02 — Baseline sin commits previos**

```bash
python3 ../sbac.py init
python3 ../sbac.py baseline v1.0
```

Salida esperada:
```
Error: No puedes definir una línea base porque no se ha creado ningún commit en el repositorio
```

Salida obtenida:
```
Error: No puedes definir una línea base porque no se ha creado ningún commit en el repositorio
```

**Estado: PASS**

---

**LB-03 — Checkout a commit por ID**

```bash
echo "contenido modificado" > archivo.txt
cat archivo.txt
python3 ../sbac.py checkout v1779939080
cat archivo.txt
```

Salida esperada: el archivo vuelve a su contenido original tras el checkout

Salida obtenida:
```
contenido modificado
Restaurado: archivo.txt
Espacio de trabajo cambiado exitosamente a 'v1779939080' (v1779939080)
contenido v1
```

**Estado: PASS**

---

**LB-04 — Checkout usando nombre de baseline**

```bash
echo "otra modificacion" > archivo.txt
cat archivo.txt
python3 ../sbac.py checkout v1.0
cat archivo.txt
```

Salida esperada: el archivo se restaura usando el nombre de la baseline en lugar del ID directo

Salida obtenida:
```
otra modificacion
Restaurado: archivo.txt
Espacio de trabajo cambiado exitosamente a 'v1.0' (v1779939080)
contenido v1
```

**Estado: PASS**

---

### 5.4 Grupo CP — Comparación entre Versiones

Este grupo verifica el comando `diff` y `list-baselines` bajo distintas condiciones

---

**CP-01 — Diff entre dos commits válidos**

```bash
python3 ../sbac.py init
echo "linea 1" > archivo.txt
python3 ../sbac.py add archivo.txt
python3 ../sbac.py commit "Commit uno"

echo "linea 1 modificada" > archivo.txt
python3 ../sbac.py add archivo.txt
python3 ../sbac.py commit "Commit dos"

python3 ../sbac.py diff v1779939492 v1779939519
```

Salida esperada: diferencias en formato unified diff con líneas `+` y `-`

Salida obtenida:
```
--- v1779939492/archivo.txt
+++ v1779939519/archivo.txt
@@ -1 +1 @@
-linea 1
+linea 1 modificada
```

**Estado: PASS**

---

**CP-02 — Diff con ID de versión inválido**

```bash
python3 ../sbac.py diff v1779939492 id_falso
```

Salida esperada:
```
Error: Uno o ambos identificadores de versión no existen...
```

Salida obtenida:
```
Error: Uno o ambos identificadores de versión no existen (v1779939492, id_falso)
```

**Estado: PASS**

---

**CP-03 — Diff sin archivos comunes entre versiones**

```bash
python3 ../sbac.py diff v1779939814 v1779939492
```

Salida esperada:
```
No se encontraron archivos comunes entre ambas versiones para comparar
```

Salida obtenida:
```
No se encontraron archivos comunes entre ambas versiones para comparar
```

> **Nota:** Durante la preparación de este caso se detectó un defecto adicional (INC-002). Al intentar crear dos commits en rápida sucesión, el sistema generó IDs idénticos causando un error. Ver sección 7

**Estado: PASS**

---

**CP-04 — Diff del mismo commit consigo mismo**

```bash
python3 ../sbac.py diff v1779939492 v1779939492
```

Salida esperada: mensaje indicando que no hay cambios

Salida obtenida:
```
El archivo 'archivo.txt' no presenta cambios entre estas versiones
```

**Estado: PASS**

---

**CP-05 — Listar baselines sin ninguna registrada**

```bash
python3 ../sbac.py list-baselines
```

Salida esperada:
```
No se han registrado líneas base en este repositorio
```

Salida obtenida:
```
No se han registrado líneas base en este repositorio
```

**Estado: PASS**

---

### 5.5 Grupo ME — Manejo de Errores

Este grupo verifica que el sistema responda correctamente ante condiciones de error, sin crashes ni comportamientos inesperados

---

**ME-01 — Ejecutar comando sin repositorio inicializado**

```bash
mkdir test_me && cd test_me
python3 ../sbac.py status
```

Salida esperada:
```
Error: El repositorio SBAC no está inicializado. Ejecuta primero 'sbac init'
```

Salida obtenida:
```
Error: El repositorio SBAC no está inicializado. Ejecuta primero 'sbac init'
```

**Estado: PASS**

---

**ME-02 — Añadir archivo que no existe**

```bash
python3 ../sbac.py init
python3 ../sbac.py add archivo_fantasma.py
```

Salida esperada:
```
Error: El archivo 'archivo_fantasma.py' no existe
```

Salida obtenida:
```
Error: El archivo 'archivo_fantasma.py' no existe
```

**Estado: PASS**

---

**ME-03 — Checkout a referencia inválida**

```bash
python3 ../sbac.py checkout etiqueta_falsa
```

Salida esperada:
```
Error: La versión o línea base 'etiqueta_falsa' no existe
```

Salida obtenida:
```
Error: La versión o línea base 'etiqueta_falsa' no existe
```

**Estado: PASS**

---

**ME-04 — Commit sin escribir el mensaje**

```bash
python3 ../sbac.py commit
```

Salida esperada: error de argparse indicando que falta el argumento

Salida obtenida:
```
usage: sbac.py commit [-h] mensaje
sbac.py commit: error: the following arguments are required: mensaje
```

**Estado: PASS**

---

**ME-05 — Diff con solo un argumento**

```bash
python3 ../sbac.py diff v1.0
```

Salida esperada: error de argparse indicando que falta el segundo argumento

Salida obtenida:
```
usage: sbac.py diff [-h] v1 v2
sbac.py diff: error: the following arguments are required: v2
```

**Estado: PASS**

---

## 6. Tabla General de Resultados

| ID | Descripción | Grupo | Estado |
|----|-------------|-------|--------|
| GR-01 | Inicializar repositorio vacío | Gestión de Repositorio | PASS |
| GR-02 | Doble inicialización | Gestión de Repositorio | PASS |
| GR-03 | Estado sin archivos añadidos | Gestión de Repositorio | PASS |
| GR-04 | Estado con archivo en el index | Gestión de Repositorio | PASS |
| GR-05 | Historial inicial vacío | Gestión de Repositorio | PASS |
| GR-06 | Consulta de ayuda principal | Gestión de Repositorio | PASS |
| CV-01 | Agregar archivo individual | Control de Versiones | PASS |
| CV-02 | Agregar archivo ya rastreado | Control de Versiones | PASS |
| CV-03 | Intentar añadir un directorio | Control de Versiones | PASS |
| CV-04 | Commit exitoso | Control de Versiones | PASS |
| CV-05 | Commit sin archivos en el index | Control de Versiones | PASS |
| CV-06 | Ver historial tras commits | Control de Versiones | PASS |
| CV-07 | Colisión de nombres en commit | Control de Versiones | FAIL |
| LB-01 | Crear línea base exitosa | Líneas Base | PASS |
| LB-02 | Baseline sin commits previos | Líneas Base | PASS |
| LB-03 | Checkout a commit por ID | Líneas Base | PASS |
| LB-04 | Checkout usando nombre de baseline | Líneas Base | PASS |
| CP-01 | Diff entre dos commits válidos | Comparación | PASS |
| CP-02 | Diff con ID de versión inválido | Comparación | PASS |
| CP-03 | Diff sin archivos comunes | Comparación | PASS |
| CP-04 | Diff del mismo commit consigo mismo | Comparación | PASS |
| CP-05 | Listar baselines sin ninguna registrada | Comparación | PASS |
| ME-01 | Ejecutar status sin repositorio | Manejo de Errores | PASS |
| ME-02 | Añadir archivo inexistente | Manejo de Errores | PASS |
| ME-03 | Checkout a referencia inválida | Manejo de Errores | PASS |
| ME-04 | Commit sin mensaje | Manejo de Errores | PASS |
| ME-05 | Diff con un solo argumento | Manejo de Errores | PASS |

| Métrica | Valor |
|---------|-------|
| Total de casos ejecutados | 27 |
| Casos PASS | 25 |
| Casos FAIL | 2 |
| Tasa de éxito | 92.6% |

---

## 7. Reporte de Incidentes y defectos encontrados

### INC-001 — Colisión de nombres en commit

**ID:** INC-001  
**Fecha de detección:** 2026-05-27  
**Caso de prueba relacionado:** CV-07  
**Severidad:** Alta  

**Descripción:**  
Cuando el usuario añade dos archivos con el mismo nombre pero en rutas distintas (por ejemplo `src/main.py` y `test/main.py`), el sistema los acepta sin error. Sin embargo, al crear el commit, ambos archivos se guardan con solo su nombre base (`main.py`), por lo que el segundo sobrescribe al primero dentro de la carpeta del commit. El sistema reporta éxito aunque se perdió un archivo de forma silenciosa e irreversible.

**Pasos para reproducir:**
```bash
sbac init
mkdir -p src test
echo "version a" > src/main.py
echo "version b" > test/main.py
sbac add src/main.py
sbac add test/main.py
sbac commit "Colision de nombres"
ls .sbac/commits/vID/
```

**Resultado esperado:** Ambos archivos guardados correctamente en el commit 
**Resultado real:** Solo aparece un `main.py` en la carpeta del commit
**Causa raíz:** En `core.py`, la función `crear_commit()` guarda los archivos usando únicamente `os.path.basename(file)`, sin considerar la ruta completa 
**Estado:** Abierto — pendiente corrección por el equipo de desarrollo

---

### INC-002 — Colisión de timestamps en IDs de versión

**ID:** INC-002  
**Fecha de detección:** 2026-05-27  
**Caso de prueba relacionado:** CP-03 (detectado durante la preparación)  
**Severidad:** Alta  

**Descripción:**  
La función `generar_id_version()` en `utils.py` crea el ID de cada commit usando el timestamp actual en segundos enteros (`int(time.time())`). Si el usuario ejecuta dos commits dentro del mismo segundo, ambos reciben el mismo ID. El segundo commit falla con un error de sistema (`FileExistsError`) sin mostrar un mensaje claro al usuario.

**Pasos para reproducir:**
```bash
sbac init
echo "a" > archivo1.txt
sbac add archivo1.txt
sbac commit "primero"
echo "b" > archivo2.txt
sbac add archivo2.txt
sbac commit "segundo"   # ejecutado de inmediato
```

**Resultado esperado:** Segundo commit creado con un ID único diferente
**Resultado real:**
```
Traceback (most recent call last):
  ...
FileExistsError: [Errno 17] File exists: '.sbac/commits/vXXXXXXXXXX'
```

**Causa raíz:** En `utils.py`, `generar_id_version()` usa `int(time.time())` con precisión de un segundo. No existe protección contra duplicados 
**Estado:** Abierto — pendiente corrección por el equipo de desarrollo

---

## 8. Pruebas de Integración

Las pruebas de integración verificaron que los tres módulos del sistema (`utils.py`, `core.py`, `sbac.py`) trabajen correctamente en conjunto a lo largo de flujos completos de múltiples pasos

### Flujo de integración 1 — Ciclo completo de versionado

```
init → add → commit → status → history
```

Se verificó que:
- `sbac init` crea la estructura de carpetas que `core.py` necesita
- `sbac add` escribe correctamente en `index.json` mediante `utils.escribir_json()`
- `sbac commit` lee el index, copia archivos y genera `meta.json`
- `sbac status` lee el index actualizado y lo muestra vacío tras el commit
- `sbac history` lee los `meta.json` de todos los commits y los ordena por fecha

**Resultado:** Flujo completo sin errores. Todos los módulos se comunicaron correctamente

---

### Flujo de integración 2 — Líneas base y restauración

```
init → add → commit → baseline → modificar archivo → checkout → verificar contenido
```

Se verificó que:
- `sbac baseline` escribe el vínculo en `baselines.json`
- `sbac checkout` resuelve el nombre de la baseline a su ID mediante `_resolver_identificador()`
- Los archivos se restauran a su contenido original desde la carpeta del commit

**Resultado:** La restauración funcionó tanto por ID directo como por nombre de baseline

---

### Flujo de integración 3 — Comparación entre versiones

```
init → add → commit (v1) → modificar → add → commit (v2) → diff v1 v2
```

Se verificó que:
- Los dos commits almacenan correctamente sus archivos en carpetas separadas
- `sbac diff` localiza los archivos comunes entre ambas versiones
- `difflib` genera correctamente el formato unified diff con líneas `+` y `-`

**Resultado:** La comparación mostró correctamente los cambios entre versiones

---

## 9. Pruebas Completas del Sistema

Se ejecutaron flujos end-to-end simulando el uso real del sistema por parte de un usuario. En cada flujo se verificaron tanto el comportamiento funcional como el manejo de errores

**Escenario 1 — Usuario inicializa y versiona archivos de código**  
El sistema aceptó la inicialización, el rastreo de archivos, la creación de versiones y la consulta del historial sin errores. Todos los mensajes fueron claros y correctos

**Escenario 2 — Usuario intenta operar sin haber inicializado**  
El sistema detectó correctamente la ausencia del repositorio y bloqueó todas las operaciones con mensajes de error descriptivos, gracias al decorador `@validar_repositorio` implementado en `core.py`

**Escenario 3 — Usuario crea línea base y regresa a una versión anterior**  
El sistema vinculó correctamente la baseline al commit activo y restauró los archivos al contenido original al ejecutar `checkout`, tanto usando el ID del commit como el nombre de la baseline

**Escenario 4 — Usuario compara dos versiones con cambios**  
El comando `diff` mostró correctamente las diferencias entre versiones usando el formato unified diff de `difflib`, indicando las líneas eliminadas con `-` y las añadidas con `+`

**Escenario 5 — Usuario provoca condiciones de error**  
El sistema manejó correctamente todos los casos de error probados: archivos inexistentes, directorios, referencias inválidas, argumentos faltantes y repositorio no inicializado, sin producir crashes en ningún caso

---

## 10. Conclusiones

### Resultados frente a criterios de aceptación

| Criterio del Plan de Pruebas | Requerido | Obtenido | Cumplido |
|-----------------------------|-----------|----------|----------|
| Tasa de éxito mínima | 95% | 92.6% | No |
| Fallos críticos (Alta/Crítica) | 0% | 2 casos | No |
| Defectos menores (Baja) | ≤ 5% | 0% | Sí |

### Análisis general

El sistema SBAC demuestra una base funcional sólida. Los 25 casos exitosos confirman que la arquitectura general es correcta y que el manejo de errores del sistema es robusto en todos los escenarios probados. Los comandos de gestión de repositorio, líneas base, comparación y manejo de errores funcionan correctamente y responden de forma clara al usuario.

Sin embargo, los dos defectos de severidad alta detectados impiden cumplir los criterios de aceptación establecidos en el Plan de pruebas maestro:

- **INC-001** representa un riesgo real de pérdida de datos para usuarios que trabajen con proyectos que tengan archivos del mismo nombre en rutas distintas
- **INC-002** puede causar fallas inesperadas del sistema en condiciones normales de uso, sobre todo en flujos automatizados o scripts

### Recomendación

Se recomienda que el equipo de desarrollo corrija ambos defectos antes de la entrega final del proyecto. Una vez corregidos y re-probados, se espera alcanzar una tasa de éxito del 100% (27/27 casos), cumpliendo todos los criterios del Plan de Pruebas Maestro

---

*Documento generado por: QA Lead / Pruebas*  
*Proyecto: SBAC — Pruebas de Software y Administración de la Configuración*  
*Fecha: Mayo de 2026*
