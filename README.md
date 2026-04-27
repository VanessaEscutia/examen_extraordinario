# Estra API

API REST en Flask para pasar mi extra con documentacion en SWAGGER en la ruta `\docs`

## Instalacion

1. Crea y activa el entorno virtual.

```bash
python -m venv env
```
Activar el Entorno Virtual

```bash
env\Scripts\activate
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Crea la BD con el nombre `estra`


5. Inicializar con `flask db init`

6. Mensaje para tu migracion `flask db migrate -m "cómo voy a lavar los tomates? si ya los puse a hervir. en agua. ya se lavaron ahí. HIRVIÓ, HIRVIÓ"`

7. Subir los cambios con `flask db upgrade`

8. Los SEEDERS estan con `flask seed run`

NOTA: Para resetear el SEED `flask --app app seed reset`


## Ejecutar la aplicacion

```bash
python app.py
```

## Swagger y documentacion

- Swagger UI: `/docs`

## Estructura del proyecto

```text
app.py                 Punto de entrada y fabrica de la app
config.py              Configuracion de base de datos
extensions.py          Inicializacion de extensiones
controllers/           Blueprints y endpoints REST
models/                Modelos SQLAlchemy
Seed/                  Seeders de datos
migrations/            Configuracion y versiones de migracion
requirements.txt       Dependencias del proyecto
```
