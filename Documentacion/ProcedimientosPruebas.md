# Procedimientos de Prueba (Test Procedure Specification) - IEEE 829

**Proyecto:** Sistema Básico de Administración de Configuración (SBAC)

**Fase:** Pruebas de Estabilización

Este documento define los pasos exactos para ejecutar la suite de 28 casos de prueba automatizados que validan los módulos GR, CV, LB, CP y ME.

---

## 1. Requisitos del Entorno

Para garantizar la correcta ejecución de los casos de prueba, el entorno de la estación de trabajo debe cumplir con lo siguiente:
*   **Intérprete:** Python 3.8 o superior.
*   **Librerías Estándar (No requieren instalación vía pip):** `unittest`, `os`, `shutil`, `sys`, `time`, `difflib`, `json`, `argparse`.
*   **Sistema Operativo:** Compatible con Windows, Linux o macOS.

## 2. Configuración Previa (Setup)

Antes de iniciar la batería de pruebas, asegúrate de cumplir con estas precondiciones:
1.  **Ubicación de Archivos:** Verifica que los archivos `core.py`, `utils.py`, `sbac.py` y `test_sbac.py` se encuentren en el mismo directorio de trabajo.
2.  **Permisos de Escritura:** El usuario que ejecute las pruebas debe tener permisos de lectura/escritura en el directorio actual, ya que las pruebas generarán carpetas (`.sbac`) y archivos de texto temporales.
3.  **Repositorio Limpio:** Si existe una carpeta `.sbac` de pruebas manuales anteriores, no es necesario borrarla manualmente; las funciones `setUp` y `tearDown` del framework se encargarán de limpiar el entorno antes de cada test.

## 3. Pasos Detallados de Ejecución

La ejecución se realiza de manera automatizada utilizando el módulo `unittest` integrado en Python.

**Paso 1: Abrir la Terminal**
Abre tu consola de comandos o terminal de preferencia y navega hasta el directorio del proyecto SBAC.
```bash
cd Proyecto-SBAC-Pruebas-de-software/sbac
```

**Paso 2: Ejecutar la Suite de Pruebas con Verbosidad**
Ejecuta el siguiente comando para lanzar los 28 casos de prueba. El flag `-v` (verbose) mostrará el nombre de cada prueba y su estado individual en tiempo real.
```bash
python -m unittest test_sbac.py -v
```

**Paso 3: Validación del Flujo Lógico (Pruebas Manuales / Exploratorias)**
Si deseas comprobar el flujo manualmente, ejecuta esta secuencia lógica en el CLI:
1.  `python sbac.py init` (Prepara el entorno)
2.  `echo "test" > prueba.txt` (Crea archivo)
3.  `python sbac.py add prueba.txt` (Añade al staging)
4.  `python sbac.py status` (Verifica el index)
5.  `python sbac.py commit "Primer commit"` (Guarda versión)
6.  `python sbac.py baseline v1.0` (Etiqueta la versión)
7.  `python sbac.py history` (Verifica la creación)
8.  `python sbac.py checkout v1.0` (Restaura)

## 4. Limpieza Post-Prueba (Teardown)

El script de pruebas automatizadas está diseñado para ser **idempotente y auto-limpiable**.
*   Al finalizar cada método de prueba, la función `tearDown` incorporada en cada clase de prueba (`TestGestionRepositorio`, `TestControlVersiones`, etc.) se invoca automáticamente.
*   Esta función elimina de forma segura el directorio oculto `.sbac` y cualquier archivo `.txt` residual (`archivo1.txt`, `archivo2.txt`, subdirectorios temporales) generado durante la prueba.
*   **Resultado:** El directorio de trabajo queda en su estado original, listo para la siguiente ronda de pruebas o para su uso en producción. No se requiere intervención manual.
