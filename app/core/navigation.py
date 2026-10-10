"""
Motor de navegación (Fase 3-4, secciones 26/34 del brief).

Contiene solo lógica de recorrido de la jerarquía Categoría -> Subcategoría
-> Comandos. No imprime nada ni sabe de input()/Tkinter/Flask: cada
interfaz decide cómo mostrar esto (Regla 34, separación DATA -> SERVICES -> INTERFACES).
"""

from dataclasses import dataclass

from app.core.search import list_by_category
from app.data.categories import CATEGORIES
from app.data.models import Category, Command, Subcategory


def get_all_categories() -> list[Category]:
    """Categorías en el orden de la taxonomía definitiva (Fase 1)."""
    return list(CATEGORIES.values())


def get_category(category_id: str) -> Category | None:
    return CATEGORIES.get(category_id)


@dataclass
class SubcategoryInfo:
    subcategory: Subcategory
    command_count: int


def get_subcategories(category_id: str) -> list[SubcategoryInfo]:
    """Subcategorías de una categoría junto con cuántos comandos tiene cada una."""
    cat = CATEGORIES.get(category_id)
    if not cat:
        return []
    infos = []
    for sub in cat.subcategories:
        count = len(list_by_category(category_id, sub.id))
        infos.append(SubcategoryInfo(sub, count))
    return infos


def get_commands(category_id: str, subcategory_id: str | None = None) -> list[Command]:
    return list_by_category(category_id, subcategory_id)
