


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