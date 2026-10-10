#!/usr/bin/env python3
"""
Punto de entrada único de Linux Command Master.

Uso:
    python run.py            -> abre la CLI interactiva (Fase 4)
    python run.py --gui      -> abre la interfaz Tkinter (Fase 5)
    python run.py --api      -> levanta la API Flask (Fase 6)
    python run.py --validate -> corre el validador de la base de datos y sale
"""

import sys


def main() -> None:
    args = sys.argv[1:]

    if "--validate" in args:
        from app.core.validator import validate_database
        report = validate_database()
        print(report.summary())
        sys.exit(0 if report.ok else 1)

    if "--gui" in args:
        from app.gui.tkinter_app import main as gui_main
        gui_main()
        return

    if "--api" in args:
        from app.api.flask_app import main as api_main
        api_main()
        return

    from app.cli.menu import main as cli_main
    cli_main()


if __name__ == "__main__":
    main()
