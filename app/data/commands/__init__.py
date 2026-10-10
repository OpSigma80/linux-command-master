"""
Diccionario maestro (sección 4 y 23 del brief).

Este módulo es el ÚNICO punto donde todos los comandos de todas las
categorías se agregan en una sola estructura indexada por id. Esto
garantiza que cada comando exista en un solo lugar (ficha maestra),
tal como exige la Regla 5.

app/core/search.py y app/core/navigation.py deben importar SIEMPRE
desde aquí (COMMANDS), nunca desde los submódulos individuales, para
que CLI, Tkinter y Flask compartan una única fuente de verdad.
"""

from app.data.models import Command

from . import (
    admin,
    compression,
    devops,
    docker,
    files,
    network,
    packages,
    permissions,
    processes,
    search,
    shell,
    system,
    text,
    utilities,
    wsl,
)

_MODULES = (
    files, text, search, permissions, processes, network, compression,
    system, admin, packages, shell, docker, devops, wsl, utilities,
)

# Diccionario maestro final: id -> Command
COMMANDS: dict[str, Command] = {}

for _module in _MODULES:
    for _cmd in _module.COMMANDS:
        COMMANDS[_cmd.id] = _cmd

__all__ = ["COMMANDS"]
