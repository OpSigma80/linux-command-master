"""
CLI interactiva (Fase 4, secciones 26 y 27 del brief).

Toda la lógica de datos viene de app/core (search.py, navigation.py).
Este módulo SOLO imprime y lee input() — cero lógica de negocio aquí,
para que Tkinter y Flask puedan reusar exactamente los mismos datos
sin duplicar reglas (Regla 34).
"""

import os

from app.core import navigation, search
from app.data.models import Command, Risk

WIDTH = 60

# Colores ANSI estándar de terminal — el mismo mecanismo que usa
# `ls --color`, `git status` o `grep --color`. Sin dependencias externas,
# funciona en cualquier terminal Linux/WSL moderna.
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_DIM = "\033[2m"
RISK_ANSI = {
    Risk.SEGURO: "\033[32m",       # verde
    Risk.PRECAUCION: "\033[33m",   # amarillo
    Risk.PELIGROSO: "\033[31;1m",  # rojo brillante
}


def _risk_label(risk: Risk) -> str:
    """Texto de riesgo coloreado con ANSI, o '' si es Seguro (no hace ruido visual)."""
    if risk == Risk.SEGURO:
        return ""
    color = RISK_ANSI[risk]
    return f" {color}[{risk.value}]{ANSI_RESET}"


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause() -> None:
    input("\nPresiona ENTER para continuar...")


def print_header() -> None:
    print("╔" + "═" * (WIDTH - 2) + "╗")
    print("║" + "LINUX COMMAND MASTER".center(WIDTH - 2) + "║")
    print("║" + "Cheatsheet • Automation • DevOps".center(WIDTH - 2) + "║")
    print("╚" + "═" * (WIDTH - 2) + "╝")


def print_main_menu() -> None:
    clear_screen()
    print_header()
    print()
    categories = navigation.get_all_categories()
    for i, cat in enumerate(categories, start=1):
        print(f"{i:>2}. {cat.name}")
    print()
    print(" B. Buscar comando")
    print(" 0. Salir")
    print()


def print_command_detail(cmd: Command) -> None:
    clear_screen()
    print("━" * WIDTH)
    print(f"COMANDO: {cmd.name}")
    print("━" * WIDTH)
    print(f"\nDescripción:\n  {cmd.description}")
    print(f"\nSintaxis:\n  {cmd.syntax}")

    if cmd.examples:
        print("\nEjemplos:")
        for ex in cmd.examples:
            print(f"  $ {ex}")

    if cmd.when_to_use:
        print(f"\nCuándo usar:\n  {cmd.when_to_use}")

    if cmd.options:
        print("\nOpciones importantes:")
        for opt in cmd.options:
            print(f"  {opt}")

    if cmd.risk != Risk.SEGURO:
        color = RISK_ANSI[cmd.risk]
        print(f"\n{color}{ANSI_BOLD}[{cmd.risk.value}]{ANSI_RESET}")
        if cmd.precautions:
            print(f"  {cmd.precautions}")

    if cmd.replaces:
        print(f"\nModernización — reemplaza a un comando más antiguo: {cmd.replaces}")
    if cmd.replaced_by:
        print(f"\nModernización — se recomienda usar en su lugar: '{cmd.replaced_by}'")

    if cmd.related:
        related = search.related_commands(cmd.id)
        names = ", ".join(r.name for r in related) if related else ", ".join(cmd.related)
        print(f"\nComandos relacionados:\n  {names}")

    print(f"\nNivel: {cmd.level.value}")
    print(f"Tags: {', '.join(cmd.tags)}")
    print("━" * WIDTH)


def command_detail_loop(cmd: Command) -> None:
    """Muestra la ficha de un comando y permite saltar a sus relacionados."""
    while True:
        print_command_detail(cmd)
        related = search.related_commands(cmd.id)
        print("\nOpciones: [ENTER] volver  ", end="")
        if related:
            print("| [1-{}] ver comando relacionado".format(len(related)))
            for i, r in enumerate(related, start=1):
                print(f"   {i}. {r.name}")
        else:
            print()

        choice = input("\n> ").strip()
        if choice == "":
            return
        if choice.isdigit() and related and 1 <= int(choice) <= len(related):
            cmd = related[int(choice) - 1]
            continue
        # entrada no reconocida: simplemente redibuja


def print_commands_list(commands: list[Command], title: str) -> Command | None:
    """Lista numerada de comandos; retorna el elegido o None si el usuario vuelve."""
    while True:
        clear_screen()
        print("━" * WIDTH)
        print(title)
        print("━" * WIDTH)
        for i, cmd in enumerate(commands, start=1):
            print(f"{i:>2}. {cmd.name:<30}{_risk_label(cmd.risk)}")
        print("\n 0. Volver")

        choice = input("\n> ").strip()
        if choice == "0":
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(commands):
            return commands[int(choice) - 1]
        # entrada inválida: vuelve a mostrar


def subcategory_menu(category_id: str) -> None:
    cat = navigation.get_category(category_id)
    if not cat:
        return
    while True:
        clear_screen()
        print("━" * WIDTH)
        print(f"{cat.name}")
        print("━" * WIDTH)
        print(f"{cat.description}\n")

        subs = navigation.get_subcategories(category_id)
        for i, info in enumerate(subs, start=1):
            print(f"{i:>2}. {info.subcategory.name} ({info.command_count})")
        print("\n 0. Volver al menú principal")

        choice = input("\n> ").strip()
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(subs):
            sub = subs[int(choice) - 1].subcategory
            commands = navigation.get_commands(category_id, sub.id)
            if not commands:
                continue
            selected = print_commands_list(commands, f"{cat.name} → {sub.name}")
            if selected:
                command_detail_loop(selected)
        # entrada inválida: vuelve a mostrar el mismo menú


def search_flow() -> None:
    clear_screen()
    print("━" * WIDTH)
    print("BUSCAR COMANDO")
    print("━" * WIDTH)
    query = input("\nEscribe tu búsqueda (ej: docker, grep, permisos): ").strip()
    if not query:
        return

    results = search.search(query, limit=15)
    if not results:
        print(f"\nNo se encontraron resultados para '{query}'.")
        pause()
        return

    commands = [r.command for r in results]
    selected = print_commands_list(commands, f"Resultados para: '{query}'")
    if selected:
        command_detail_loop(selected)


def main() -> None:
    try:
        _main_loop()
    except (KeyboardInterrupt, EOFError):
        print("\n\nHasta luego.")


def _main_loop() -> None:
    while True:
        print_main_menu()
        choice = input("> ").strip().upper()

        if choice == "0":
            print("\nHasta luego.")
            break
        if choice == "B":
            search_flow()
            continue

        categories = navigation.get_all_categories()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            selected_cat = categories[int(choice) - 1]
            subcategory_menu(selected_cat.id)
        # entrada inválida: vuelve a mostrar el menú principal


if __name__ == "__main__":
    main()
