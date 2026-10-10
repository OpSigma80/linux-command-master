# API Reference

The Flask API exposes the exact same data and logic used by the CLI and
GUI (`app/core`) as JSON over HTTP. Start it with:

    python run.py --api

By default it runs on `http://localhost:5000`.

## Language parameter

Every endpoint below accepts an optional `?lang=es|en` query parameter
(default: `es`). If a command hasn't been translated to English yet, it
automatically falls back to Spanish for that command only -- the request
never fails because of a missing translation.

## GET /

Returns basic info about the API and the dataset.

    curl http://localhost:5000/

```json
{
  "name": "Linux Command Master API",
  "endpoints": ["/categories", "/categories/<category>", "..."],
  "total_commands": 236,
  "total_categories": 16
}
```

## GET /categories

Returns all 16 categories with their subcategories and command counts.

    curl http://localhost:5000/categories
    curl http://localhost:5000/categories?lang=en

```json
[
  {
    "id": "docker",
    "name": "Docker",
    "description": "Contenedores, imagenes, compose, redes y volumenes.",
    "subcategories": [
      {"id": "containers", "name": "Contenedores", "command_count": 6},
      {"id": "images", "name": "Imagenes", "command_count": 5}
    ]
  }
]
```

## GET /categories/\<category_id\>

Returns one category plus the full list of its commands.

    curl http://localhost:5000/categories/docker

Returns `404` with `{"error": "category_not_found"}` if the id doesn't exist.

## GET /commands

Returns commands. Supports optional filters, combinable:

- `?category=<id>`
- `?subcategory=<id>`
- `?tag=<id>`

    curl http://localhost:5000/commands
    curl "http://localhost:5000/commands?category=docker&tag=maintenance"

## GET /commands/\<command_id\>

Returns a single command's full entry.

    curl http://localhost:5000/commands/rm

```json
{
  "id": "rm",
  "name": "rm",
  "category": "files",
  "subcategory": "filesops",
  "description": "Elimina archivos o directorios de forma permanente (sin papelera).",
  "syntax": "rm [opciones] archivo",
  "examples": ["rm archivo.txt", "rm -r carpeta/", "rm -rf carpeta/"],
  "when_to_use": "Borrado definitivo de archivos o directorios.",
  "options": ["-r (recursivo)", "-f (forzar, sin confirmar)"],
  "precautions": "rm -rf no tiene papelera de reciclaje: verifica SIEMPRE la ruta...",
  "related": ["rmdir", "mv"],
  "tags": ["filesystem"],
  "level": "Básico",
  "risk": "Peligroso",
  "replaces": null,
  "replaced_by": null
}
```

Returns `404` with `{"error": "command_not_found"}` if the id doesn't exist.

## GET /search?q=\<query\>

Fuzzy search with relevance ranking (exact id match scores highest, then
name, then tag, then description).

    curl "http://localhost:5000/search?q=docker"

Each result includes `score` (0-100) and `matched_on` (why it matched),
in addition to the full command fields.

Returns `400` with `{"error": "missing_query"}` if `q` is missing or empty.

## GET /tags/\<tag_id\>

Returns a tag's description plus every command that has it.

    curl http://localhost:5000/tags/docker

Returns `404` with `{"error": "tag_not_found"}` if the tag isn't registered
(see `app/data/tags.py` for the canonical tag list).

## Error format

All errors are JSON, never Flask's default HTML error page:

```json
{"error": "command_not_found", "command": "whatever_was_requested"}
```
