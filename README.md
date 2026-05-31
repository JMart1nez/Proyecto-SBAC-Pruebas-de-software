# SBAC (Sistema Básico de Administración de Configuración)

## Resumen del Proyecto
El **Sistema Básico de Administración de Configuración (SBAC)** es una herramienta de Interfaz de Línea de Comandos (CLI) desarrollada en Python. Su objetivo principal es demostrar y aplicar los conceptos fundamentales de la Administración de Configuración (AC) de software, ofreciendo un entorno controlado, directo y educativo que elimina las complejidades inherentes a sistemas de control de versiones comerciales más grandes (como Git).

## Integrantes del Equipo Rojo
El proyecto fue desarrollado de forma colaborativa siguiendo buenas prácticas de ingeniería de software, contando con los siguientes roles fundamentales:

* **Martínez Leal José María** 
* **Matú Hernández Diana** 
* **Olivares Díaz Belen** 
* **Sánchez Cruz Norma Selene** 
* **Sánchez Pavia Angel Gabriel** 

## ⚙️ Requisitos Previos
Para poder utilizar SBAC, asegúrate de contar con lo siguiente en tu entorno de desarrollo:
* **Python 3** (versión 3.x o superior) instalado en tu sistema.
* Acceso a una **Terminal**.

## Tecnologías Utilizadas
* **Lenguaje Principal:** Python 3.
* **Librerías Estándar de Python:** 
  * `difflib`: Utilizada para el núcleo funcional del comando `diff`, permitiendo la comparación y el análisis visual de las versiones de archivos.
  * `os`, `sys`, `shutil`, `json`: Manejo del sistema de archivos, parseo de argumentos CLI y persistencia de metadatos.
* **Pruebas (Testing):** Uso intensivo del framework `unittest` para la automatización y ejecución estructurada de la suite de calidad.

## Guía de Instalación y Ejecución

1. **Clonar o descargar el repositorio:**
   ```bash
   git clone https://github.com/JMart1nez/Proyecto-SBAC-Pruebas-de-software.git
   cd Proyecto-SBAC-Pruebas-de-software
   ```

2. **Ejecutar el sistema:**
   El código fuente se encuentra dentro del directorio `sbac/`. Para ejecutar el sistema, navega a esa carpeta y utiliza el archivo `sbac.py`:
   ```bash
   cd sbac
   python sbac.py <comando>
   ```

## Estructura del Directorio
El repositorio refleja la siguiente estructura real de archivos y directorios:

```text
.
├── Documentacion/   # Documentación IEEE 829, manuales de usuario y métricas de calidad
└── sbac/            # Directorio principal del código fuente y pruebas
    ├── .sbac/       # Directorio oculto de metadatos e historial (generado con init)
    ├── sbac.py      # CLI: Punto de entrada principal para el usuario
    ├── core.py      # Lógica de negocio y manejo de metadatos del repositorio
    ├── utils.py     # Funciones auxiliares y utilidades del sistema
    └── test_sbac.py # Suite automatizada con 28 casos de prueba (unittest)
```

## Comandos Disponibles

SBAC soporta 9 comandos fundamentales para la administración de la configuración:

| Comando | Descripción | Ejemplo de Uso |
| :--- | :--- | :--- |
| `init` | Inicializa un nuevo repositorio creando el directorio de control `.sbac/`. | `python sbac.py init` |
| `add` | Añade un archivo (o sus cambios) al área de preparación (staging area). | `python sbac.py add <archivo>` |
| `status` | Muestra el estado actual del área de preparación y los archivos modificados. | `python sbac.py status` |
| `commit` | Guarda los cambios del área de preparación de manera permanente en el historial. | `python sbac.py commit "Mensaje descriptivo"` |
| `history` | Muestra el log y el historial completo de commits realizados. | `python sbac.py history` |
| `baseline` | Crea una línea base estable o hito a partir de un commit específico. | `python sbac.py baseline <commit_id> "Nombre"` |
| `list-baselines`| Muestra todas las líneas base documentadas en el repositorio. | `python sbac.py list-baselines` |
| `diff` | Muestra las diferencias de código entre un archivo local y su última versión en el commit anterior. | `python sbac.py diff <archivo>` |
| `checkout` | Restaura el espacio de trabajo a un estado, commit o línea base específica. | `python sbac.py checkout <commit_id>` |

## Calidad y Estándares
Este proyecto fue diseñado con un fuerte énfasis en el Aseguramiento de Calidad (QA) y el rigor metodológico:
* **Estándar IEEE 829:** Toda la documentación del ciclo de pruebas (PlandePruebasMaestro, DiseñoPruebasIniciales, ProcedimientosPruebas, ReporteResumenPruebas, Reporte_Incidentes) se rige bajo los formatos estructurados de la norma IEEE 829.
* **Norma ISO/IEC 25010:** La implementación del código y las pruebas garantizan que el software cumpla con atributos y subcaracterísticas de calidad, priorizando fuertemente la **Adecuación Funcional**, la **Mantenibilidad** y la **Confiabilidad** del sistema.
