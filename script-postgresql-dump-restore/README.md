# pgdumpres: Herramienta de Backup y Restauración de Bases de Datos 💽

## Descripción 📑

`pgdumpres` es una herramienta código python que permite realizar copias de seguridad y restauraciones de bases de datos PostgreSQL. Proporciona varias opciones para hacer dumps completos, dumps comprimidos, dumps de esquemas y dumps de roles. También permite restaurar archivos de dump tanto comprimidos como no comprimidos.

## Uso 💻

El script admite las siguientes opciones y argumentos:

### Parámetros de configuración

- `--host`: Dirección del servidor de la base de datos (requerido).
- `--user`: Usuario de la base de datos (requerido).
- `--password`: Contraseña de la base de datos (opcional, si no se proporciona se solicitará interactivamente).
- `--db`: Nombre de la base de datos (requerido, salvo para dump de roles).
- `--dumpFile`: Nombre del archivo de dump para restauración (requerido para restauraciones. Un dump genera un dumpFile dinámicamente).

### Parámetros de acciones

- `--dumpRole`: Realizar un dump de los roles de la base de datos.
- `--dumpSchema`: Realizar un dump del esquema de la base de datos.
- `--dumpFull`: Realizar un dump completo de la base de datos.
- `--dumpFullCompress`: Realizar un dump completo de la base de datos y comprimirlo.
- `--restore`: Restaurar un archivo no comprimido con `psql`.
- `--restoreCompress`: Restaurar un archivo comprimido con `pg_restore`.

## Ejemplos 📜

### Dump de Roles

Para realizar un dump de los roles de la base de datos:

```sh
python pgdumpres.py --host 127.0.0.1  --user miusuario --password "password" --dumpRole
# Si no se proporciona --password, se solicitará interactivamente
```

### Dump Completo de la Base de Datos

Para realizar un dump completo de la base de datos:

```sh
python pgdumpres.py --host 127.0.0.1 --user miusuario --db mibasedatos --password "password" --dumpFull
# Si no se proporciona --password, se solicitará interactivamente
```

### Dump Comprimido de la Base de Datos

Para realizar un dump completo de la base de datos y comprimirlo:

```sh
python pgdumpres.py --host 127.0.0.1 --user miusuario --db mibasedatos --password "password" --dumpFullCompress
# Si no se proporciona --password, se solicitará interactivamente
```

### Dump del Esquema de la Base de Datos

Para realizar un dump del esquema de la base de datos:

```sh
python pgdumpres.py --host 127.0.0.1 --user miusuario --db mibasedatos --password "password" --dumpSchema
# Si no se proporciona --password, se solicitará interactivamente
```

### Restaurar desde un Archivo No Comprimido

Para restaurar una base de datos desde un archivo de dump no comprimido:

```sh
python pgdumpres.py --host 127.0.0.1 --user miusuario --dumpFile backup_file.sql --password "password" --restore
# Si no se proporciona --password, se solicitará interactivamente
```

### Restaurar desde un Archivo Comprimido

Para restaurar una base de datos desde un archivo de dump comprimido:

```sh
python pgdumpres.py --host 127.0.0.1 --user miusuario --dumpFile backup_file.dump --password "password" --restoreCompress
# Si no se proporciona --password, se solicitará interactivamente
```
