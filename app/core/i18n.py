"""
Internacionalización (i18n) — Fase de traducción ES/EN.

DISEÑO: el español sigue siendo la ÚNICA fuente de verdad de los datos
(app/data/commands/*.py no se duplica). Las traducciones al inglés viven
en diccionarios SEPARADOS, indexados por el mismo id que ya usa cada
comando/categoría/tag. Si una traducción no existe todavía (porque aún
no llegamos a esa categoría en la Fase B), el sistema cae de vuelta al
español automáticamente — nunca rompe la app por una traducción faltante.

    ES (fuente de verdad, siempre completa)
         ↓
    Capa de traducción EN (parcial, crece por fases)
         ↓
    CLI / GUI piden texto vía t_command(), t_category(), etc.
"""

from enum import Enum

from app.data.models import Level, Risk


class Lang(str, Enum):
    ES = "es"
    EN = "en"


# --------------------------------------------------------------------- #
# Textos fijos de interfaz (menús, botones, encabezados) — CLI y GUI
# --------------------------------------------------------------------- #
UI_TEXT: dict[str, dict[Lang, str]] = {
    "app_title": {Lang.ES: "Linux Command Master", Lang.EN: "Linux Command Master"},
    "app_subtitle": {Lang.ES: "Cheatsheet • Automation • DevOps",
                      Lang.EN: "Cheatsheet • Automation • DevOps"},
    "home": {Lang.ES: "Inicio", Lang.EN: "Home"},
    "back": {Lang.ES: "← Atrás", Lang.EN: "← Back"},
    "search_placeholder": {Lang.ES: "Buscar comando (ej: docker, grep, permisos)...",
                            Lang.EN: "Search command (e.g: docker, grep, permissions)..."},
    "search_results_for": {Lang.ES: "Resultados para", Lang.EN: "Results for"},
    "no_results": {Lang.ES: "Sin resultados.", Lang.EN: "No results."},
    "welcome_hint": {
        Lang.ES: "Selecciona una categoría en el panel izquierdo o busca un comando arriba.",
        Lang.EN: "Select a category on the left panel or search for a command above.",
    },
    "description": {Lang.ES: "Descripción", Lang.EN: "Description"},
    "syntax": {Lang.ES: "Sintaxis", Lang.EN: "Syntax"},
    "examples": {Lang.ES: "Ejemplos", Lang.EN: "Examples"},
    "when_to_use": {Lang.ES: "Cuándo usar", Lang.EN: "When to use"},
    "options": {Lang.ES: "Opciones importantes", Lang.EN: "Important options"},
    "precaution": {Lang.ES: "Precaución", Lang.EN: "Caution"},
    "modernization": {Lang.ES: "Modernización", Lang.EN: "Modernization"},
    "replaces": {Lang.ES: "Reemplaza al comando más antiguo",
                 Lang.EN: "Replaces the older command"},
    "replaced_by": {Lang.ES: "Se recomienda usar en su lugar",
                    Lang.EN: "It's recommended to use instead"},
    "related": {Lang.ES: "Comandos relacionados", Lang.EN: "Related commands"},
    "copy": {Lang.ES: "Copiar", Lang.EN: "Copy"},
    "copied": {Lang.ES: "✓ Copiado", Lang.EN: "✓ Copied"},
    "level": {Lang.ES: "Nivel", Lang.EN: "Level"},
    "search_menu": {Lang.ES: "Buscar comando", Lang.EN: "Search command"},
    "exit": {Lang.ES: "Salir", Lang.EN: "Exit"},
    "back_menu": {Lang.ES: "Volver", Lang.EN: "Back"},
    "back_to_main": {Lang.ES: "Volver al menú principal", Lang.EN: "Back to main menu"},
    "goodbye": {Lang.ES: "Hasta luego.", Lang.EN: "Goodbye."},
    "search_prompt": {Lang.ES: "Escribe tu búsqueda (ej: docker, grep, permisos): ",
                       Lang.EN: "Type your search (e.g: docker, grep, permissions): "},
    "no_results_for": {Lang.ES: "No se encontraron resultados para", Lang.EN: "No results found for"},
    "tags_label": {Lang.ES: "Tags", Lang.EN: "Tags"},
}


def t_ui(key: str, lang: Lang) -> str:
    """Traduce un texto fijo de interfaz. Si falta la traducción, cae a ES."""
    entry = UI_TEXT.get(key, {})
    return entry.get(lang) or entry.get(Lang.ES, key)


# --------------------------------------------------------------------- #
# Niveles y riesgo — sets fijos (4 y 3 valores), fáciles de traducir 100%
# --------------------------------------------------------------------- #
LEVEL_EN: dict[Level, str] = {
    Level.BASICO: "Basic",
    Level.INTERMEDIO: "Intermediate",
    Level.AVANZADO: "Advanced",
    Level.EXPERTO: "Expert",
}

RISK_EN: dict[Risk, str] = {
    Risk.SEGURO: "Safe",
    Risk.PRECAUCION: "Caution",
    Risk.PELIGROSO: "Dangerous",
}


def t_level(level: Level, lang: Lang) -> str:
    return LEVEL_EN[level] if lang == Lang.EN else level.value


def t_risk(risk: Risk, lang: Lang) -> str:
    return RISK_EN[risk] if lang == Lang.EN else risk.value


# --------------------------------------------------------------------- #
# Categorías y subcategorías (16 categorías — set pequeño, se traduce
# completo de una vez, a diferencia de los 236 comandos que van por fases)
# --------------------------------------------------------------------- #
CATEGORY_EN: dict[str, dict] = {
    "files": {
        "name": "File Navigation & Management",
        "description": "Move around the filesystem and manage files/directories.",
        "subcategories": {
            "nav": "Navigation", "dirs": "Directories", "filesops": "Files",
            "links": "Links and paths", "advanced": "Advanced management",
        },
    },
    "text": {
        "name": "Text Reading & Manipulation",
        "description": "View, edit, filter and transform text content.",
        "subcategories": {
            "view": "Viewing", "editors": "Text editors", "filter": "Filtering and transformation",
            "process": "Processing", "diff": "Comparison", "streams": "Streams and redirections",
        },
    },
    "search": {
        "name": "Search",
        "description": "Locate files, content, processes or commands.",
        "subcategories": {"find-content": "Files and content", "find-commands": "Commands and executables"},
    },
    "permissions": {
        "name": "Permissions, Users & Identity",
        "description": "Access control, ownership, users and groups.",
        "subcategories": {"perms": "Permissions", "users": "Users and groups", "identity": "Identity and session"},
    },
    "processes": {
        "name": "Processes & Performance",
        "description": "Process management, jobs and real-time monitoring.",
        "subcategories": {"proc": "Processes", "jobs": "Jobs", "resources": "Real-time resources"},
    },
    "network": {
        "name": "Networking",
        "description": "Diagnostics, configuration, transfer, remote access and network security.",
        "subcategories": {
            "diagnostics": "Diagnostics", "config": "Configuration",
            "transfer": "Transfer and remote access", "ssh-advanced": "Advanced SSH and sessions",
            "netsecurity": "Network security",
        },
    },
    "compression": {
        "name": "Compression & Archives",
        "description": "Package and compress files and directories.",
        "subcategories": {"archive": "Compression and decompression"},
    },
    "system": {
        "name": "System Information",
        "description": "Static hardware, kernel, distro and storage information.",
        "subcategories": {
            "hardware": "Hardware and kernel", "distro": "Distribution",
            "storage": "Storage", "env": "Environment",
        },
    },
    "admin": {
        "name": "System Administration",
        "description": "Services, logs, boot, mounting and scheduled tasks.",
        "subcategories": {
            "services": "Services", "logs": "Logs", "boot": "Boot/mount",
            "scheduling": "Task scheduling",
        },
    },
    "packages": {
        "name": "Package Management",
        "description": "Installing and managing system and Python software.",
        "subcategories": {"apt": "Debian/Ubuntu/WSL", "python-env": "Python/Conda environments"},
    },
    "shell": {
        "name": "Shell, Scripting & Automation",
        "description": "Bash, flow control, debugging and real automation patterns.",
        "subcategories": {
            "basics": "Bash fundamentals", "debugging": "Control and debugging",
            "patterns": "Automation patterns",
        },
    },
    "docker": {
        "name": "Docker",
        "description": "Containers, images, compose, networks and volumes.",
        "subcategories": {
            "containers": "Containers", "images": "Images", "compose": "Docker Compose",
            "net-vol": "Networks and volumes", "diagnostics": "Diagnostics",
        },
    },
    "devops": {
        "name": "DevOps",
        "description": "Version control and DevOps workflow.",
        "subcategories": {"git": "Git"},
    },
    "maintenance": {
        "name": "Maintenance & Cleanup",
        "description": (
            "Cross-cutting view: groups by 'maintenance' tag commands that already "
            "exist in Packages, Administration, Docker and System. Defines no new "
            "commands, avoids duplicating entries."
        ),
        "subcategories": {"safe": "Safe cleanup", "advanced": "Advanced cleanup", "destructive": "Potentially destructive cleanup"},
    },
    "wsl": {
        "name": "WSL — Optimization & Administration",
        "description": "Management and performance of WSL/Debian on Windows.",
        "subcategories": {"management": "Distro management", "performance": "Performance and configuration"},
    },
    "utilities": {
        "name": "Utilities & Help",
        "description": "System documentation and various shell utilities.",
        "subcategories": {"help": "Help and documentation", "misc": "Miscellaneous utilities"},
    },
}


def t_category_name(category_id: str, lang: Lang) -> str:
    from app.data.categories import CATEGORIES
    if lang == Lang.EN and category_id in CATEGORY_EN:
        return CATEGORY_EN[category_id]["name"]
    return CATEGORIES[category_id].name


def t_category_description(category_id: str, lang: Lang) -> str:
    from app.data.categories import CATEGORIES
    if lang == Lang.EN and category_id in CATEGORY_EN:
        return CATEGORY_EN[category_id]["description"]
    return CATEGORIES[category_id].description


def t_subcategory_name(category_id: str, subcategory_id: str, lang: Lang) -> str:
    from app.data.categories import CATEGORIES
    if lang == Lang.EN and category_id in CATEGORY_EN:
        en_sub = CATEGORY_EN[category_id]["subcategories"].get(subcategory_id)
        if en_sub:
            return en_sub
    cat = CATEGORIES[category_id]
    for sub in cat.subcategories:
        if sub.id == subcategory_id:
            return sub.name
    return subcategory_id


# --------------------------------------------------------------------- #
# Tags (sección 24) — nombres cortos ya están en inglés (ej: "network",
# "docker"); solo traducimos su DESCRIPCIÓN larga.
# --------------------------------------------------------------------- #
TAG_EN: dict[str, str] = {
    "navigation": "File and directory navigation",
    "filesystem": "File system",
    "text": "Text manipulation",
    "editor": "Text editors",
    "search": "Searching files, content or processes",
    "permissions": "Permissions and ownership",
    "users": "Users, groups and identity",
    "processes": "Processes and jobs",
    "performance": "Real-time performance and monitoring",
    "network": "Networking",
    "remote": "Remote access (SSH, file transfer)",
    "security": "Security, firewall, encryption, scanning",
    "compression": "Compression and archiving",
    "system-info": "Static system/hardware information",
    "storage": "Disks, partitions and storage",
    "admin": "System administration, services, systemd",
    "scheduling": "Scheduled tasks (cron, timers)",
    "packages": "Package management",
    "python-env": "Python / Conda / Jupyter environments",
    "bash": "Bash syntax and fundamentals",
    "scripting": "General scripting",
    "automation": "Real automation patterns",
    "docker": "Docker and containers",
    "devops": "Git, CI/CD, deployment",
    "wsl": "Windows Subsystem for Linux",
    "maintenance": "System cleanup and maintenance",
    "help": "Help and documentation",
    "utility": "Various shell utilities",
    "modernized": "Command with a modern replacement (Rule 4)",
}


def t_tag(tag_id: str, lang: Lang) -> str:
    from app.data.tags import TAGS
    if lang == Lang.EN and tag_id in TAG_EN:
        return TAG_EN[tag_id]
    return TAGS.get(tag_id, tag_id)


# --------------------------------------------------------------------- #
# Comandos (236 fichas, Fase B en progreso — ver app/data/i18n_commands/)
# --------------------------------------------------------------------- #
class TranslatedCommand:
    """
    Vista de solo lectura de un Command en el idioma pedido. Combina la
    ficha ES (fuente de verdad) con su traducción EN parcial: cada campo
    usa la traducción si existe, y cae automáticamente al español si esa
    categoría aún no fue traducida (Fase B en progreso). Los campos
    estructurales (id, category, subcategory, tags, level, risk, related,
    replaces, replaced_by) NUNCA se traducen — son identificadores, no
    texto para el usuario.
    """

    def __init__(self, command, lang: Lang):
        self._cmd = command
        self._lang = lang
        from app.data.i18n_commands import COMMAND_EN
        self._en = COMMAND_EN.get(command.id, {}) if lang == Lang.EN else {}

    def _f(self, field: str):
        return self._en.get(field, getattr(self._cmd, field))

    @property
    def id(self): return self._cmd.id
    @property
    def category(self): return self._cmd.category
    @property
    def subcategory(self): return self._cmd.subcategory
    @property
    def tags(self): return self._cmd.tags
    @property
    def related(self): return self._cmd.related
    @property
    def replaces(self): return self._cmd.replaces
    @property
    def replaced_by(self): return self._cmd.replaced_by

    @property
    def name(self): return self._f("name")
    @property
    def description(self): return self._f("description")
    @property
    def syntax(self): return self._f("syntax")
    @property
    def examples(self): return self._f("examples")
    @property
    def when_to_use(self): return self._f("when_to_use")
    @property
    def options(self): return self._f("options")
    @property
    def precautions(self): return self._f("precautions")

    @property
    def level_label(self) -> str:
        return t_level(self._cmd.level, self._lang)

    @property
    def risk_label(self) -> str:
        return t_risk(self._cmd.risk, self._lang)

    @property
    def risk(self):
        return self._cmd.risk  # el enum crudo, para comparar (== Risk.SEGURO, etc)


def t_command(command, lang: Lang) -> TranslatedCommand:
    """Punto de entrada único: envuelve un Command con su traducción."""
    return TranslatedCommand(command, lang)
