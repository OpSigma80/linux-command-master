<img width="1257" height="693" alt="Captura de pantalla 2026-10-10 154718" src="https://github.com/user-attachments/assets/9c8ecedd-b6ed-4b4d-96c1-f4f5f6973ba9" />

# Linux Command Master

An interactive cheatsheet and advanced command finder for Linux, focused
on Debian/Ubuntu/WSL, shell scripting, automation, DevOps, Docker,
networking and security. Built in pure Python, no unnecessary frameworks.

This isn't just a list of commands: every entry includes syntax, real
examples, when to use it, important options, a risk level, and related
commands.

## Features

- **236 commands** organized into 16 categories, no duplicates -- every
  command lives in a single master entry, cross-referenced by tags from
  other categories when relevant.
- **Search with relevance ranking** (exact id -> name -> tag -> description).
- **Automatic data integrity validator** (--validate).
- **Interactive CLI** with category browsing and search.
- **Desktop GUI (Tkinter)** with a navigation tree, detail panel,
  copy-to-clipboard, and color-coded risk indicators.
- **Bilingual (ES/EN)** with a live language switch -- categories not
  translated yet automatically fall back to Spanish without breaking the
  interface (translation in progress, see app/data/i18n_commands/).
- Commands flagged by risk level (Safe / Caution / Dangerous), with
  explicit warnings on potentially destructive ones.

## Installation

Requires Python 3.10+.

    git clone https://github.com/OpSigma80/linux-command-master.git
    cd linux-command-master
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

The GUI also needs python3-tk at the system level (not included by
default on Debian):

    sudo apt install python3-tk

### Tux mascot (optional)

The GUI shows Tux in the bottom-right corner. The image isn't included in
the repository (it's an external asset, not project code):

    mkdir -p app/gui/assets
    curl -sL -A "Mozilla/5.0" -o app/gui/assets/tux.png "https://upload.wikimedia.org/wikipedia/commons/a/af/Tux.png"

If it's not downloaded, the app still works fine -- just without the icon.

## Usage

    python run.py              # interactive CLI
    python run.py --gui        # graphical interface (Tkinter)
    python run.py --api        # REST API (see docs/API.md), port 5000
    python run.py --validate   # validates the database and exits

## Running tests

    pip install -r requirements-dev.txt
    python -m pytest tests/ -v

## Architecture

    DATA (app/data)
       |
    CORE ENGINE (app/core: search.py, navigation.py, validator.py, i18n.py)
       |
       +-- CLI (app/cli)
       +-- GUI (app/gui)
       +-- Flask API (app/api)

CLI and GUI share the exact same search, navigation and translation
logic -- no interface duplicates business rules.

## Documentation

- [API Reference](docs/API.md) -- all 6 endpoints with real examples
- [Contributing](CONTRIBUTING.md) -- how to add commands/categories/translations

## Project status

- [DONE] Phases 1-5: taxonomy, master dictionary, validator/search, CLI, GUI
- [DONE] Phase 6: Flask API (6 endpoints, bilingual)
- [DONE] Phase 7: automated tests (65 tests, pytest)
- [IN PROGRESS] Phase 9: EN translation, 10 of 16 categories (141/236 commands)
- [PENDING] Phase 9: code cleanup pass

## Notes

Source code comments and docstrings are in Spanish (the developer's
primary language); user-facing text (README, commit history, and the app
itself) is bilingual/English-first.

## License

MIT -- see [LICENSE](LICENSE). Tux is the Linux mascot created by Larry
Ewing, used here under its own free-use license (see the note at the
bottom of the LICENSE file).
