


## INC-001

**ID:** INC-001

**Fecha:** 2026-05-27

**Caso relacionado:** CV-07

**Severidad:** Alta

**Descripción:** Al hacer commit de dos archivos con el mismo nombre
en rutas distintas, el sistema sobrescribe el primero con el segundo
sin advertir al usuario. El commit reporta éxito pero hay pérdida
de datos silenciosa.

**Pasos para reproducir:**
1. sbac init
2. echo "version a" > src/main.py
3. echo "version b" > test/main.py
4. sbac add src/main.py
5. sbac add test/main.py
6. sbac commit "Colision de nombres"
7. ls .sbac/commits/vID/
   
**Resultado esperado:** Ambos archivos guardados en el commit

**Resultado real:** Solo aparece un main.py en la carpeta del commit

**Estado:** Abierto



## INC-002

**ID:** INC-002

**Fecha:** 2026-05-27

**Caso relacionado:** CP-03

**Severidad:** Alta

**Descripción:** Si dos commits se ejecutan dentro del mismo segundo,
el sistema genera IDs idénticos. El segundo commit falla con
FileExistsError y no se guarda, pero no muestra un mensaje de error
claro al usuario.
**Pasos para reproducir:**
1. sbac init
2. sbac add archivo1.txt
3. sbac commit "primero"
4. sbac add archivo2.txt
5. sbac commit "segundo"  ← ejecutado inmediatamente después
**Resultado esperado:** Segundo commit creado con ID único

**Resultado real:** FileExistsError - el commit no se guarda

**Estado:** Abierto



## INC-003

**ID:** INC-003

**Fecha:** 2026-05-28

**Caso relacionado:** CP-03

**Severidad:** Media

**Descripción:** La función `diff` omite los archivos que fueron añadidos o eliminados entre dos commits. Solo compara archivos que existen en ambas versiones, ocultando cambios importantes al usuario.
**Pasos para reproducir:**
1. sbac add a.txt && sbac commit "v1"
2. sbac add b.txt && sbac commit "v2"
3. sbac diff <ID_V1> <ID_V2>
**Resultado esperado:** Notificación de adición de `b.txt` (+)

**Resultado real:** Mensaje "No se encontraron archivos comunes". Se omite `b.txt`.

**Estado:** Abierto



## INC-004

**ID:** INC-004

**Fecha:** 2026-05-28

**Caso relacionado:** ME-01

**Severidad:** Media

**Descripción:** El sistema no emite código de error del sistema (Exit Code 1) cuando el decorador `@validar_repositorio` falla. Retorna 0 (Éxito), lo cual engaña a scripts de CI/CD haciendo que pruebas fallidas parezcan exitosas.
**Pasos para reproducir:** 
1. En directorio vacío: `sbac status`
2. Revisar exit code: `echo $?` (Linux)
**Resultado esperado:** Exit code 1

**Resultado real:** Exit code 0

**Estado:** Abierto



## INC-005

**ID:** INC-005

**Fecha:** 2026-05-28

**Caso relacionado:** LB-03 (Observación de Auditoría)

**Severidad:** Media

**Descripción:** "Estado Sucio" al restaurar. El comando `checkout` copia los archivos viejos al espacio de trabajo pero no elimina los archivos nuevos no rastreados que el usuario haya creado después, mezclando versiones.

**Estado:** Abierto



## INC-006

**ID:** INC-006

**Fecha:** 2026-05-28

**Caso relacionado:** CV-04 (Lógica Core)

**Severidad:** Crítica

**Descripción:** Pérdida de historial entre versiones. La función `crear_commit` solo empaqueta los archivos presentes en el `index.json`, sin heredar los archivos del commit anterior. Cada versión es una cápsula aislada; al hacer checkout a un nuevo commit, se pierden los archivos de commits pasados.

**Estado:** Abierto

