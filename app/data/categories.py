"""
Registro de las 16 categorías principales (taxonomía definitiva, Fase 1).

Este módulo solo define METADATOS de navegación (nombre, descripción,
subcategorías). Los comandos viven en app/data/commands/ y apuntan
aquí mediante Command.category / Command.subcategory.
"""

from app.data.models import Category, Subcategory

CATEGORIES: dict[str, Category] = {

    "files": Category(
        id="files", name="Navegación y Gestión de Archivos", icon="📁",
        description="Moverse por el sistema de archivos y gestionar archivos/directorios.",
        subcategories=[
            Subcategory("nav", "Navegación"),
            Subcategory("dirs", "Directorios"),
            Subcategory("filesops", "Archivos"),
            Subcategory("links", "Enlaces y rutas"),
            Subcategory("advanced", "Gestión avanzada"),
        ],
    ),

    "text": Category(
        id="text", name="Lectura y Manipulación de Texto", icon="📝",
        description="Ver, editar, filtrar y transformar contenido de texto.",
        subcategories=[
            Subcategory("view", "Visualización"),
            Subcategory("editors", "Edición de texto"),
            Subcategory("filter", "Filtrado y transformación"),
            Subcategory("process", "Procesamiento"),
            Subcategory("diff", "Comparación"),
            Subcategory("streams", "Streams y redirecciones"),
        ],
    ),

    "search": Category(
        id="search", name="Búsqueda", icon="🔎",
        description="Localizar archivos, contenido, procesos o comandos.",
        subcategories=[
            Subcategory("find-content", "Archivos y contenido"),
            Subcategory("find-commands", "Comandos y ejecutables"),
        ],
    ),

    "permissions": Category(
        id="permissions", name="Permisos, Usuarios e Identidad", icon="🔐",
        description="Control de acceso, propiedad, usuarios y grupos.",
        subcategories=[
            Subcategory("perms", "Permisos"),
            Subcategory("users", "Usuarios y grupos"),
            Subcategory("identity", "Identidad y sesión"),
        ],
    ),

    "processes": Category(
        id="processes", name="Procesos y Rendimiento", icon="⚙️",
        description="Gestión de procesos, jobs y monitorización en tiempo real.",
        subcategories=[
            Subcategory("proc", "Procesos"),
            Subcategory("jobs", "Jobs"),
            Subcategory("resources", "Recursos en tiempo real"),
        ],
    ),

    "network": Category(
        id="network", name="Redes", icon="🌐",
        description="Diagnóstico, configuración, transferencia, acceso remoto y seguridad de red.",
        subcategories=[
            Subcategory("diagnostics", "Diagnóstico"),
            Subcategory("config", "Configuración"),
            Subcategory("transfer", "Transferencia y acceso remoto"),
            Subcategory("ssh-advanced", "SSH avanzado y sesiones"),
            Subcategory("netsecurity", "Seguridad de red"),
        ],
    ),

    "compression": Category(
        id="compression", name="Compresión y Archivos", icon="🗜️",
        description="Empaquetar y comprimir archivos y directorios.",
        subcategories=[
            Subcategory("archive", "Compresión y descompresión"),
        ],
    ),

    "system": Category(
        id="system", name="Información del Sistema", icon="🖥️",
        description="Información estática de hardware, kernel, distro y almacenamiento.",
        subcategories=[
            Subcategory("hardware", "Hardware y kernel"),
            Subcategory("distro", "Distribución"),
            Subcategory("storage", "Almacenamiento"),
            Subcategory("env", "Entorno"),
        ],
    ),

    "admin": Category(
        id="admin", name="Administración del Sistema", icon="🛠️",
        description="Servicios, logs, arranque, montaje y tareas programadas.",
        subcategories=[
            Subcategory("services", "Servicios"),
            Subcategory("logs", "Logs"),
            Subcategory("boot", "Boot/mount"),
            Subcategory("scheduling", "Programación de tareas"),
        ],
    ),

    "packages": Category(
        id="packages", name="Gestión de Paquetes", icon="📦",
        description="Instalación y gestión de software del sistema y de Python.",
        subcategories=[
            Subcategory("apt", "Debian/Ubuntu/WSL"),
            Subcategory("python-env", "Entornos Python/Conda"),
        ],
    ),

    "shell": Category(
        id="shell", name="Shell, Scripting y Automatización", icon="🐚",
        description="Bash, control de flujo, debugging y patrones reales de automatización.",
        subcategories=[
            Subcategory("basics", "Fundamentos Bash"),
            Subcategory("debugging", "Control y debugging"),
            Subcategory("patterns", "Patrones de automatización"),
        ],
    ),

    "docker": Category(
        id="docker", name="Docker", icon="🐳",
        description="Contenedores, imágenes, compose, redes y volúmenes.",
        subcategories=[
            Subcategory("containers", "Contenedores"),
            Subcategory("images", "Imágenes"),
            Subcategory("compose", "Docker Compose"),
            Subcategory("net-vol", "Redes y volúmenes"),
            Subcategory("diagnostics", "Diagnóstico"),
        ],
    ),

    "devops": Category(
        id="devops", name="DevOps", icon="🚀",
        description="Control de versiones y flujo de trabajo DevOps.",
        subcategories=[
            Subcategory("git", "Git"),
        ],
    ),

    "maintenance": Category(
        id="maintenance", name="Mantenimiento y Limpieza", icon="🧹",
        description=(
            "Vista transversal: agrupa por tag 'maintenance' comandos que ya "
            "existen en Paquetes, Administración, Docker y Sistema. No define "
            "comandos nuevos, evita duplicar fichas."
        ),
        subcategories=[
            Subcategory("safe", "Limpieza segura"),
            Subcategory("advanced", "Limpieza avanzada"),
            Subcategory("destructive", "Limpieza potencialmente destructiva"),
        ],
    ),

    "wsl": Category(
        id="wsl", name="WSL — Optimización y Administración", icon="🪟",
        description="Gestión y rendimiento de WSL/Debian sobre Windows.",
        subcategories=[
            Subcategory("management", "Gestión de distros"),
            Subcategory("performance", "Rendimiento y configuración"),
        ],
    ),

    "utilities": Category(
        id="utilities", name="Utilidades y Ayuda", icon="🧰",
        description="Documentación del sistema y utilidades varias de shell.",
        subcategories=[
            Subcategory("help", "Ayuda y documentación"),
            Subcategory("misc", "Utilidades varias"),
        ],
    ),
}
