"""
Agregador de traducciones EN de comandos (Fase 9, en progreso).

Cada categoria traducida agrega su modulo aqui. Categorias aun no
traducidas simplemente no aparecen -- sus comandos caen de vuelta al
espanol automaticamente (ver app/core/i18n.py: t_command).

PROGRESO: 10 de 16 categorias traducidas (files, text, search, permissions,
processes, compression, admin, system, packages, utilities = 141/236 comandos).
"""

from . import (
    admin_en,
    compression_en,
    files_en,
    packages_en,
    permissions_en,
    processes_en,
    search_en,
    system_en,
    text_en,
    utilities_en,
)

_MODULES = (
    files_en,
    text_en,
    search_en,
    permissions_en,
    processes_en,
    compression_en,
    admin_en,
    system_en,
    packages_en,
    utilities_en,
)

COMMAND_EN: dict[str, dict] = {}
for _module in _MODULES:
    COMMAND_EN.update(_module.COMMAND_EN)

__all__ = ["COMMAND_EN"]
