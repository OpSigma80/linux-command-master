"""
Modelo de datos central de Linux Command Master.

Este módulo NO contiene comandos ni categorías: solo define la
estructura (el "contrato") que toda la base de conocimiento debe
respetar. Los datos reales viven en app/data/commands/*.py y
app/data/categories.py.

Diseño:
    DATOS (dataclasses) -> motor de navegación/búsqueda -> interfaces
"""

from dataclasses import dataclass, field
from enum import Enum


class Level(str, Enum):
    """Nivel de dificultad/uso de un comando."""
    BASICO = "Básico"
    INTERMEDIO = "Intermedio"
    AVANZADO = "Avanzado"
    EXPERTO = "Experto"


class Risk(str, Enum):
    """Nivel de riesgo de un comando (Regla 7 y 29). Texto plano: cada
    interfaz decide cómo señalar el riesgo con SU propio medio (color
    ANSI en la CLI, color de texto en Tkinter) — no con emoji de colores."""
    SEGURO = "Seguro"
    PRECAUCION = "Precaución"
    PELIGROSO = "Peligroso"


@dataclass
class Command:
    """
    Ficha maestra de UN comando. Debe existir una sola instancia por
    comando real (Regla 5 y sección 23 de duplicados); otras categorías
    lo referencian por su `id` dentro de sus tags/related, nunca
    duplicando la ficha completa.
    """
    id: str                          # identificador único, ej: "grep"
    name: str                        # nombre mostrado, ej: "grep"
    category: str                    # id de categoría "dueña" (ficha maestra)
    subcategory: str                 # id de subcategoría dentro de esa categoría
    description: str                 # explicación clara y breve
    syntax: str                      # sintaxis general
    examples: list[str] = field(default_factory=list)
    when_to_use: str = ""
    options: list[str] = field(default_factory=list)   # flags importantes
    precautions: str = ""            # obligatorio si risk != SEGURO
    related: list[str] = field(default_factory=list)    # ids de otros comandos
    tags: list[str] = field(default_factory=list)        # ver app/data/tags.py
    level: Level = Level.BASICO
    risk: Risk = Risk.SEGURO
    replaces: str | None = None      # ej: "ifconfig" reemplazado por "ip"
    replaced_by: str | None = None   # ej: "netstat" -> replaced_by="ss"
    deprecated: bool = False


@dataclass
class Subcategory:
    id: str
    name: str
    description: str = ""


@dataclass
class Category:
    """
    Categoría principal del menú. NO contiene los comandos directamente
    (eso vive en app/data/commands/*.py y se enlaza vía Command.category).
    Esto evita el problema de "categorías dueñas de datos duplicados".
    """
    id: str
    name: str
    description: str
    subcategories: list[Subcategory] = field(default_factory=list)
    icon: str = "📁"
