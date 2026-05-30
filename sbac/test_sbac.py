import unittest
import os
import shutil
import sys
import time

# Aseguramos que Python encuentre core.py y utils.py en la misma carpeta
sys.path.insert(0, os.path.dirname(__file__))
import core
import utils


class TestGestionRepositorio(unittest.TestCase):
    """Casos GR-01 al GR-06: Inicialización, estado e historial."""

    def setUp(self):
        """Antes de cada prueba: entorno limpio."""
        if os.path.exists(utils.SBAC_DIR):
            shutil.rmtree(utils.SBAC_DIR)

    def tearDown(self):
        """Después de cada prueba: limpia archivos y repositorio."""
        if os.path.exists(utils.SBAC_DIR):
            shutil.rmtree(utils.SBAC_DIR)
        for f in ["archivo1.txt", "archivo2.txt", "a_f.txt", "b_f.txt"]:
            if os.path.exists(f):
                os.remove(f)

    # GR-01
    def test_GR01_inicializar_repositorio_vacio(self):
        """Inicializar en directorio limpio crea la estructura correcta."""
        core.inicializar_repositorio()
        self.assertTrue(os.path.exists(utils.SBAC_DIR))
        self.assertTrue(os.path.exists(utils.COMMITS_DIR))
        self.assertTrue(os.path.exists(utils.INDEX_FILE))
        self.assertTrue(os.path.exists(utils.BASELINES_FILE))
        self.assertTrue(os.path.exists(utils.HEAD_FILE))

    # GR-02
    def test_GR02_doble_inicializacion_no_falla(self):
        """Llamar init dos veces no rompe el repositorio existente."""
        core.inicializar_repositorio()
        # Segunda llamada no debe lanzar excepción
        try:
            core.inicializar_repositorio()
        except Exception as e:
            self.fail(f"Segunda inicialización lanzó excepción: {e}")
        self.assertTrue(os.path.exists(utils.SBAC_DIR))

    # GR-03
    def test_GR03_status_sin_archivos(self):
        """Status con index vacío no debe lanzar excepción."""
        core.inicializar_repositorio()
        try:
            core.mostrar_estado()
        except Exception as e:
            self.fail(f"mostrar_estado() lanzó excepción inesperada: {e}")

    # GR-04
    def test_GR04_status_con_archivo_en_index(self):
        """Archivo añadido debe aparecer en el index."""
        core.inicializar_repositorio()
        with open("archivo1.txt", "w") as f:
            f.write("contenido")
        core.anadir_archivo("archivo1.txt")
        index = utils.leer_json(utils.INDEX_FILE, [])
        self.assertIn("archivo1.txt", index)

    # GR-05
    def test_GR05_historial_inicial_vacio(self):
        """Historial sin commits no debe lanzar excepción."""
        core.inicializar_repositorio()
        try:
            core.mostrar_historial()
        except Exception as e:
            self.fail(f"mostrar_historial() lanzó excepción inesperada: {e}")

    # GR-06
    def test_GR06_sin_repositorio_status_falla_controlado(self):
        """Ejecutar status sin init debe fallar de forma controlada (sin crash)."""
        # No inicializamos el repositorio
        try:
            core.mostrar_estado()
        except SystemExit:
            pass  # Salida controlada es aceptable
        except Exception as e:
            self.fail(f"Falló de forma no controlada: {e}")


class TestControlVersiones(unittest.TestCase):
    """Casos CV-01 al CV-07: add, commit, history."""

    def setUp(self):
        if os.path.exists(utils.SBAC_DIR):
            shutil.rmtree(utils.SBAC_DIR)
        core.inicializar_repositorio()

    def tearDown(self):
        if os.path.exists(utils.SBAC_DIR):
            shutil.rmtree(utils.SBAC_DIR)
        for f in ["archivo1.txt", "archivo2.txt"]:
            if os.path.exists(f):
                os.remove(f)
        # Limpiar subcarpetas de prueba CV-07
        for d in ["subdir_a", "subdir_b"]:
            if os.path.exists(d):
                shutil.rmtree(d)

    def _crear_archivo(self, nombre, contenido="texto de prueba"):
        with open(nombre, "w") as f:
            f.write(contenido)

    def _hacer_commit(self, archivo, mensaje):
        self._crear_archivo(archivo)
        core.anadir_archivo(archivo)
        core.crear_commit(mensaje)

    # CV-01
    def test_CV01_agregar_archivo_individual(self):
        """Añadir un archivo existente lo registra en el index."""
        self._crear_archivo("archivo1.txt")
        core.anadir_archivo("archivo1.txt")
        index = utils.leer_json(utils.INDEX_FILE, [])
        self.assertIn("archivo1.txt", index)

    # CV-02
    def test_CV02_agregar_archivo_ya_rastreado(self):
        """Añadir el mismo archivo dos veces no lo duplica en el index."""
        self._crear_archivo("archivo1.txt")
        core.anadir_archivo("archivo1.txt")
        core.anadir_archivo("archivo1.txt")
        index = utils.leer_json(utils.INDEX_FILE, [])
        self.assertEqual(index.count("archivo1.txt"), 1)

    # CV-03
    def test_CV03_intentar_agregar_directorio(self):
        """Intentar añadir un directorio no debe romper el sistema."""
        os.makedirs("subdir_a", exist_ok=True)
        try:
            core.anadir_archivo("subdir_a")
        except Exception as e:
            self.fail(f"anadir_archivo() con directorio lanzó excepción no controlada: {e}")
        # El directorio no debe estar en el index
        index = utils.leer_json(utils.INDEX_FILE, [])
        self.assertNotIn("subdir_a", index)

    # CV-04
    def test_CV04_commit_exitoso(self):
        """Un commit con archivos en el index crea la carpeta de versión y limpia el index."""
        self._hacer_commit("archivo1.txt", "commit inicial")
        # El index debe quedar vacío
        index = utils.leer_json(utils.INDEX_FILE, [])
        self.assertEqual(index, [])
        # HEAD debe apuntar a algo
        head = utils.leer_texto(utils.HEAD_FILE)
        self.assertTrue(head.startswith("v"))
        # La carpeta del commit debe existir
        self.assertTrue(os.path.exists(os.path.join(utils.COMMITS_DIR, head)))

    # CV-05
    def test_CV05_commit_sin_archivos_en_index(self):
        """Commit con index vacío no debe crear ninguna versión."""
        core.crear_commit("commit vacío")
        commits = os.listdir(utils.COMMITS_DIR)
        self.assertEqual(commits, [])

    # CV-06
    def test_CV06_historial_tras_commits(self):
        """Historial con commits registrados no debe lanzar excepción."""
        self._hacer_commit("archivo1.txt", "primer commit")
        try:
            core.mostrar_historial()
        except Exception as e:
            self.fail(f"mostrar_historial() lanzó excepción: {e}")

    # CV-07
    def test_CV07_colision_nombres_en_commit(self):
        """
        Bug conocido: dos archivos con el mismo nombre en distintas carpetas.
        Solo uno sobrevive en la carpeta del commit.
        Este test documenta el comportamiento actual (fallo esperado).
        """
        os.makedirs("subdir_a", exist_ok=True)
        os.makedirs("subdir_b", exist_ok=True)
        with open("subdir_a/archivo1.txt", "w") as f:
            f.write("versión A")
        with open("subdir_b/archivo1.txt", "w") as f:
            f.write("versión B")

        core.anadir_archivo("subdir_a/archivo1.txt")
        core.anadir_archivo("subdir_b/archivo1.txt")
        core.crear_commit("commit con colisión")

        head = utils.leer_texto(utils.HEAD_FILE)
        commit_path = os.path.join(utils.COMMITS_DIR, head)
        archivos_en_commit = os.listdir(commit_path)

        # Debe haber 3 archivos: meta.json, subdir_a_archivo1.txt y subdir_b_archivo1.txt
        self.assertEqual(len(archivos_en_commit), 3, "No se guardaron ambos archivos.")


class TestLineasBase(unittest.TestCase):
    """Casos LB-01 al LB-04: baseline y checkout."""

    def setUp(self):
        if os.path.exists(utils.SBAC_DIR):
            shutil.rmtree(utils.SBAC_DIR)
        core.inicializar_repositorio()

    def tearDown(self):
        if os.path.exists(utils.SBAC_DIR):
            shutil.rmtree(utils.SBAC_DIR)
        if os.path.exists("archivo1.txt"):
            os.remove("archivo1.txt")

    def _hacer_commit(self, nombre="archivo1.txt", contenido="v1", mensaje="commit"):
        with open(nombre, "w") as f:
            f.write(contenido)
        core.anadir_archivo(nombre)
        core.crear_commit(mensaje)
        return utils.leer_texto(utils.HEAD_FILE)

    # LB-01
    def test_LB01_crear_linea_base_exitosa(self):
        """Crear baseline sobre un commit válido la registra correctamente."""
        self._hacer_commit()
        head = utils.leer_texto(utils.HEAD_FILE)
        core.crear_linea_base("v1.0")
        baselines = utils.leer_json(utils.BASELINES_FILE, {})
        self.assertIn("v1.0", baselines)
        self.assertEqual(baselines["v1.0"], head)

    # LB-02
    def test_LB02_crear_baseline_sin_commits(self):
        """Crear baseline sin commits previos no debe registrar nada."""
        core.crear_linea_base("v1.0")
        baselines = utils.leer_json(utils.BASELINES_FILE, {})
        self.assertNotIn("v1.0", baselines)

    # LB-03
    def test_LB03_checkout_a_commit_exitoso(self):
        """Checkout a un commit válido restaura los archivos."""
        commit_id = self._hacer_commit(contenido="contenido original")
        # Modificamos el archivo en disco
        with open("archivo1.txt", "w") as f:
            f.write("contenido modificado")
        # Restauramos
        core.restaurar_version(commit_id)
        with open("archivo1.txt", "r") as f:
            contenido = f.read()
        self.assertEqual(contenido, "contenido original")

    # LB-04
    def test_LB04_checkout_a_linea_base(self):
        """Checkout usando nombre de baseline restaura correctamente."""
        self._hacer_commit(contenido="version baseline")
        core.crear_linea_base("release-1.0")
        # Modificamos el archivo
        with open("archivo1.txt", "w") as f:
            f.write("version modificada")
        # Checkout por nombre de baseline
        core.restaurar_version("release-1.0")
        with open("archivo1.txt", "r") as f:
            contenido = f.read()
        self.assertEqual(contenido, "version baseline")


class TestComparacion(unittest.TestCase):
    """Casos CP-01 al CP-06: diff y list-baselines."""

    def setUp(self):
        if os.path.exists(utils.SBAC_DIR):
            shutil.rmtree(utils.SBAC_DIR)
        core.inicializar_repositorio()

    def tearDown(self):
        if os.path.exists(utils.SBAC_DIR):
            shutil.rmtree(utils.SBAC_DIR)
        for f in ["archivo1.txt", "archivo2.txt"]:
            if os.path.exists(f):
                os.remove(f)

    def _hacer_commit(self, nombre, contenido, mensaje):
        with open(nombre, "w") as f:
            f.write(contenido)
        core.anadir_archivo(nombre)
        time.sleep(1)  # Evita IDs de versión idénticos por timestamp
        core.crear_commit(mensaje)
        return utils.leer_texto(utils.HEAD_FILE)

    # CP-01
    def test_CP01_diff_entre_dos_commits_validos(self):
        """Diff entre dos commits con el mismo archivo no debe lanzar excepción."""
        id1 = self._hacer_commit("archivo1.txt", "linea 1\n", "v1")
        id2 = self._hacer_commit("archivo1.txt", "linea 1\nlinea 2\n", "v2")
        try:
            core.ver_diferencias(id1, id2)
        except Exception as e:
            self.fail(f"ver_diferencias() lanzó excepción: {e}")

    # CP-02
    def test_CP02_diff_con_version_inexistente(self):
        """Diff con un ID inválido no debe crashear el sistema."""
        id1 = self._hacer_commit("archivo1.txt", "contenido", "v1")
        try:
            core.ver_diferencias(id1, "id_falso_xyz")
        except Exception as e:
            self.fail(f"ver_diferencias() con ID inválido lanzó excepción: {e}")

    # CP-03
    def test_CP03_diff_sin_archivos_comunes(self):
        """Diff entre commits con archivos distintos no debe crashear."""
        id1 = self._hacer_commit("archivo1.txt", "contenido a", "v1")
        id2 = self._hacer_commit("archivo2.txt", "contenido b", "v2")
        try:
            core.ver_diferencias(id1, id2)
        except Exception as e:
            self.fail(f"ver_diferencias() sin archivos comunes lanzó excepción: {e}")

    # CP-04
    def test_CP04_diff_archivos_sin_cambios(self):
        """Diff del mismo commit consigo mismo no debe lanzar excepción."""
        id1 = self._hacer_commit("archivo1.txt", "sin cambios\n", "v1")
        try:
            core.ver_diferencias(id1, id1)
        except Exception as e:
            self.fail(f"ver_diferencias() mismo commit lanzó excepción: {e}")

    # CP-05
    def test_CP05_listar_baselines_vacio(self):
        """Listar baselines sin ninguna registrada no debe lanzar excepción."""
        try:
            core.listar_lineas_base()
        except Exception as e:
            self.fail(f"listar_lineas_base() lanzó excepción: {e}")

    # CP-06
    def test_CP06_diff_entre_lineas_base(self):
        """Diff usando nombres de líneas base en lugar de IDs de commit."""
        core.inicializar_repositorio()

        with open("archivo1.txt", "w") as f:
            f.write("linea 1\n")
        core.anadir_archivo("archivo1.txt")
        core.crear_commit("commit 1")
        core.crear_linea_base("v1.0") # Primera línea base

        with open("archivo1.txt", "a") as f:
            f.write("linea 2\n")
        core.anadir_archivo("archivo1.txt")
        core.crear_commit("commit 2")
        core.crear_linea_base("v2.0") # Segunda línea base

        try:
            core.ver_diferencias("v1.0", "v2.0")
        except Exception as e:
            self.fail(f"ver_diferencias() crasheó al intentar comparar líneas base: {e}")


class TestManejoErrores(unittest.TestCase):
    """Casos ME-01 al ME-05: manejo de errores y casos límite."""

    def setUp(self):
        if os.path.exists(utils.SBAC_DIR):
            shutil.rmtree(utils.SBAC_DIR)

    def tearDown(self):
        if os.path.exists(utils.SBAC_DIR):
            shutil.rmtree(utils.SBAC_DIR)
        if os.path.exists("archivo1.txt"):
            os.remove("archivo1.txt")

    # ME-01
    def test_ME01_status_sin_init(self):
        """Status sin repositorio inicializado falla de forma controlada."""
        try:
            core.mostrar_estado()
        except SystemExit:
            pass
        except Exception as e:
            self.fail(f"Fallo no controlado sin repositorio: {e}")

    # ME-02
    def test_ME02_agregar_archivo_inexistente(self):
        """Añadir archivo que no existe no modifica el index."""
        core.inicializar_repositorio()
        core.anadir_archivo("no_existe.py")
        index = utils.leer_json(utils.INDEX_FILE, [])
        self.assertNotIn("no_existe.py", index)

    # ME-03
    def test_ME03_checkout_inexistente(self):
        """Checkout a referencia inválida no debe crashear."""
        core.inicializar_repositorio()
        try:
            core.restaurar_version("etiqueta_falsa")
        except Exception as e:
            self.fail(f"restaurar_version() con ID inválido lanzó excepción: {e}")

    # ME-04
    def test_ME04_commit_sin_mensaje_vacio(self):
        """Commit con mensaje vacío pero index con archivos igual debe crear versión."""
        core.inicializar_repositorio()
        with open("archivo1.txt", "w") as f:
            f.write("contenido")
        core.anadir_archivo("archivo1.txt")
        core.crear_commit("")  # Mensaje vacío — no debe crashear
        head = utils.leer_texto(utils.HEAD_FILE)
        self.assertTrue(head.startswith("v"))

    # ME-05
    def test_ME05_add_archivo_inexistente_no_modifica_index(self):
        """
        Intento de add con ruta inválida deja el index intacto.
        (Equivalente funcional al error de argparse con argumento faltante.)
        """
        core.inicializar_repositorio()
        index_antes = utils.leer_json(utils.INDEX_FILE, [])
        core.anadir_archivo("ruta/inexistente/archivo.txt")
        index_despues = utils.leer_json(utils.INDEX_FILE, [])
        self.assertEqual(index_antes, index_despues)


if __name__ == "__main__":
    unittest.main(verbosity=2)
