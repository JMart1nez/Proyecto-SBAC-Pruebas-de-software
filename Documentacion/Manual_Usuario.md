# Manual de Usuario - SBAC (Sistema Básico de Administración de Configuración)

## 1. Introducción
Bienvenido a **SBAC**, una herramienta de Interfaz de Línea de Comandos (CLI) desarrollada en Python. SBAC te permite mantener un control de versiones básico de tus archivos de código, realizar seguimientos de tus cambios, crear líneas base y comparar distintas etapas de tu proyecto sin la complejidad de sistemas robustos como Git.

## 2. Requisitos Previos
*   Tener instalado **Python 3** en el sistema.
*   Acceso a una terminal de comandos.
*   El archivo principal del sistema (`sbac.py`) y sus dependencias en tu entorno de trabajo.

---

## 3. Guía de Comandos Disponibles

A continuación se detalla la sintaxis y el propósito de cada comando disponible en SBAC. Para ejecutar un comando, debes invocar el script principal con Python: `python sbac.py <comando>`.

### 3.1 Gestión del Entorno de Trabajo

**`init` - Inicializar un repositorio**
*   **Descripción:** Prepara el directorio actual para ser rastreado por SBAC creando una carpeta oculta `.sbac`.
*   **Uso:** `python sbac.py init`

**`status` - Consultar el estado**
*   **Descripción:** Muestra los archivos que han sido agregados al área de seguimiento (Staging Area) y que están listos para ser guardados en la próxima versión.
*   **Uso:** `python sbac.py status`

### 3.2 Control de Versiones

**`add` - Añadir archivos al seguimiento**
*   **Descripción:** Prepara un archivo específico para ser incluido en el próximo commit. *(Nota: Actualmente no soporta agregar directorios completos).*
*   **Uso:** `python sbac.py add <nombre_del_archivo>`
*   **Ejemplo:** `python sbac.py add main.py`

**`commit` - Guardar una nueva versión**
*   **Descripción:** Empaqueta permanentemente los archivos que fueron añadidos con `add`, creando una nueva versión en el historial. Requiere un mensaje descriptivo.
*   **Uso:** `python sbac.py commit "Mensaje descriptivo"`
*   **Ejemplo:** `python sbac.py commit "Se agregó la función de suma"`

**`history` - Ver el historial de versiones**
*   **Descripción:** Muestra una lista cronológica de todos los commits realizados, indicando su ID único (ej. `v177993...`), fecha, mensaje y archivos incluidos.
*   **Uso:** `python sbac.py history`

### 3.3 Comparación y Restauración

**`diff` - Mostrar diferencias entre versiones**
*   **Descripción:** Compara los archivos comunes entre dos versiones distintas y muestra las líneas que fueron agregadas (`+`) o eliminadas (`-`).
*   **Uso:** `python sbac.py diff <ID_version_1> <ID_version_2>`
*   **Ejemplo:** `python sbac.py diff v1234567890 v0987654321`

**`checkout` - Restaurar una versión anterior**
*   **Descripción:** Regresa el espacio de trabajo actual al estado de una versión específica del pasado. **Advertencia:** Los archivos no guardados podrían sobrescribirse.
*   **Uso:** `python sbac.py checkout <ID_version_o_linea_base>`

### 3.4 Líneas Base (Baselines)

**`baseline` - Marcar una versión estable**
*   **Descripción:** Asigna una etiqueta fácil de recordar (como `Release-1.0`) a la versión actual, para no tener que memorizar el ID numérico del commit.
*   **Uso:** `python sbac.py baseline <nombre_etiqueta>`
*   **Ejemplo:** `python sbac.py baseline Entrega_Final`

**`list-baselines` - Listar las líneas base**
*   **Descripción:** Muestra todas las etiquetas creadas y a qué ID de versión apuntan.
*   **Uso:** `python sbac.py list-baselines`

---

## 4. Flujo de Trabajo de Ejemplo (Paso a Paso)

Si eres un usuario nuevo, sigue este flujo básico para crear tu primera versión:

1. **Inicializa el proyecto:**
   ```bash
   python sbac.py init
   ```
2. **Crea o modifica un archivo:**
   ```bash
   echo "Hola Mundo" > saludo.txt
   ```
3. **Añade el archivo al seguimiento de SBAC:**
   ```bash
   python sbac.py add saludo.txt
   ```
4. **Verifica que esté listo para guardarse:**
   ```bash
   python sbac.py status
   ```
5. **Guarda tu primera versión:**
   ```bash
   python sbac.py commit "Versión inicial del saludo"
   ```
6. **Revisa tu historial para confirmar que se guardó:**
   ```bash
   python sbac.py history
   ```

---

## 5. Solución de Problemas Frecuentes (FAQ / Troubleshooting)

Durante el ciclo de desarrollo y pruebas de SBAC, identificamos y solucionamos varios incidentes. Si experimentas comportamientos inesperados, consulta esta guía:

> **Problema:** Ejecuto un comando como `sbac status` y mi sistema de integración continua reporta un fallo, o el script se detiene.
> **Solución (INC-004):** Asegúrate de haber ejecutado `sbac init` primero. SBAC ahora devuelve un código de error de sistema (`Exit Code 1`) si intentas operar fuera de un repositorio inicializado, para evitar corrupción de datos.

> **Problema:** Tenía dos archivos con el mismo nombre en diferentes carpetas (ej. `src/main.py` y `test/main.py`), los añadí al mismo tiempo, ¿se van a sobrescribir en el historial?
> **Solución (INC-001):** No. SBAC sanitiza las rutas internamente reemplazando las barras por guiones bajos (ej. `src_main.py`). Tus archivos están seguros y se restaurarán en sus carpetas correctas al usar `checkout`.

> **Problema:** Hice un script automatizado que lanza muchos `commits` por segundo y falló.
> **Solución (INC-002):** Este comportamiento fue parcheado. SBAC ahora genera IDs de versión con precisión de milisegundos, por lo que puedes ejecutar commits concurrentes sin provocar colisiones de tiempo.

> **Problema:** Al hacer `diff` entre dos versiones, el sistema crashea si en la versión 2 eliminé un archivo que existía en la versión 1.
> **Solución (INC-003):** Esto ha sido resuelto. El comando `diff` ahora reporta elegantemente los archivos que fueron `[+] Añadidos` o `[-] Eliminados` antes de intentar comparar el contenido interno de los archivos.

> **Problema:** Hice `checkout` a una versión anterior, pero en mi carpeta aún veo archivos nuevos que creé después de esa versión ("Estado Sucio").
> **Solución (INC-005):** Actualiza tu versión de SBAC. En la última versión estable, el comando `checkout` primero limpia rigurosamente el entorno eliminando archivos de la versión actual antes de restaurar los de la versión objetivo.

> **Problema:** Hice un commit modificando solo el `archivo B`, pero al hacer `checkout`, el `archivo A` del commit anterior desapareció.
> **Solución (INC-006):** Este error arquitectónico está corregido. Ahora, cada nuevo commit "hereda" y arrastra consigo los archivos de la versión inmediatamente anterior, manteniendo tu proyecto completo.


