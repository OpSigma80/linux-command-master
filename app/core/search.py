"""
Motor de búsqueda (Fase 3, sección 25 del brief).

Es la ÚNICA lógica de búsqueda del proyecto. CLI, Tkinter y Flask deben
importar de aquí, nunca reimplementar su propio filtrado (Regla 34).
"""

from dataclasses import dataclass

from app.data.categories import CATEGORIES
from app.data.commands import COMMANDS
from app.data.models import Command


@dataclass
class SearchResult:
    command: Command
    score: int
    matched_on: str  # explica por qué hizo match, útil para depurar/mostrar


def search(query: str, limit: int = 10) -> list[SearchResult]:
    """
    Búsqueda difusa por relevancia sobre id, nombre, descripción, tags y
    comandos relacionados. No requiere coincidencia exacta.
    """
    q = query.strip().lower()
    if not q:
        return []

    results: list[SearchResult] = []

    for cmd in COMMANDS.values():
        cmd_id = cmd.id.lower()
        name = cmd.name.lower()

        if cmd_id == q:
            results.append(SearchResult(cmd, 100, "id exacto"))
            continue
        if name == q:
            results.append(SearchResult(cmd, 95, "nombre exacto"))
            continue
        if cmd_id.startswith(q):
            results.append(SearchResult(cmd, 85, "id empieza con la búsqueda"))
            continue
        if name.startswith(q):
            results.append(SearchResult(cmd, 80, "nombre empieza con la búsqueda"))
            continue
        if q in [t.lower() for t in cmd.tags]:
            results.append(SearchResult(cmd, 70, f"tag '{q}'"))
            continue
        if q in cmd_id or q in name:
            results.append(SearchResult(cmd, 60, "coincide dentro del id/nombre"))
            continue
        if q in cmd.description.lower():
            results.append(SearchResult(cmd, 40, "coincide en la descripción"))
            continue
        if any(q in t.lower() for t in cmd.tags):
            results.append(SearchResult(cmd, 35, "coincide parcialmente en tags"))
            continue
        if q in [r.lower() for r in cmd.related]:
            results.append(SearchResult(cmd, 20, "es 'relacionado' de otro comando"))
            continue

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:limit]


def search_by_tag(tag: str) -> list[Command]:
    """Todos los comandos que tengan exactamente ese tag."""
    tag = tag.strip().lower()
    return [c for c in COMMANDS.values() if tag in [t.lower() for t in c.tags]]


def get_command(command_id: str) -> Command | None:
    """Ficha maestra de un comando por su id exacto."""
    return COMMANDS.get(command_id.strip().lower())


def list_by_category(category_id: str, subcategory_id: str | None = None) -> list[Command]:
    """Comandos de una categoría, opcionalmente filtrados por subcategoría."""
    result = [c for c in COMMANDS.values() if c.category == category_id]
    if subcategory_id:
        result = [c for c in result if c.subcategory == subcategory_id]
    return sorted(result, key=lambda c: c.name.lower())


def autocomplete(prefix: str, limit: int = 8) -> list[str]:
    """Sugerencias de ids que empiezan con el prefijo, para búsqueda incremental."""
    prefix = prefix.strip().lower()
    if not prefix:
        return []
    matches = [c.id for c in COMMANDS.values() if c.id.lower().startswith(prefix)]
    return sorted(matches)[:limit]


def related_commands(command_id: str) -> list[Command]:
    """Resuelve los ids de 'related' de un comando a sus objetos Command completos."""
    cmd = get_command(command_id)
    if not cmd:
        return []
    return [COMMANDS[r] for r in cmd.related if r in COMMANDS]


if __name__ == "__main__":
    demo_queries = ["docker", "grep", "permisos", "network", "ssh"]
    for dq in demo_queries:
        print(f"\n🔎 Buscar: {dq}")
        for r in search(dq, limit=5):
            cat_name = CATEGORIES[r.command.category].name
            print(f"   [{r.score:>3}] {r.command.name:<25} ({cat_name}) — match: {r.matched_on}")
