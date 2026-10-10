"""
Registro canónico de tags (sección 24).

Un comando puede tener varios tags para ser encontrado desde distintas
categorías sin duplicar su ficha (ej: 'grep' vive en 02-texto pero
tiene tag 'search' y 'automation' para aparecer también ahí).

El validador (Fase 3) usará esta lista para rechazar tags inventados
que no estén registrados aquí -> evita "tags fantasma".
"""

TAGS: dict[str, str] = {
    "navigation": "Navegación de archivos y directorios",
    "filesystem": "Sistema de archivos",
    "text": "Manipulación de texto",
    "editor": "Editores de texto",
    "search": "Búsqueda de archivos, contenido o procesos",
    "permissions": "Permisos y propiedad",
    "users": "Usuarios, grupos e identidad",
    "processes": "Procesos y jobs",
    "performance": "Rendimiento y monitorización en tiempo real",
    "network": "Redes",
    "remote": "Acceso remoto (SSH, transferencia de archivos)",
    "security": "Seguridad, firewall, cifrado, escaneo",
    "compression": "Compresión y archivado",
    "system-info": "Información estática del sistema/hardware",
    "storage": "Discos, particiones y almacenamiento",
    "admin": "Administración del sistema, servicios, systemd",
    "scheduling": "Tareas programadas (cron, timers)",
    "packages": "Gestión de paquetes",
    "python-env": "Entornos Python / Conda / Jupyter",
    "bash": "Sintaxis y fundamentos de Bash",
    "scripting": "Scripting general",
    "automation": "Patrones de automatización real",
    "docker": "Docker y contenedores",
    "devops": "Git, CI/CD, despliegue",
    "wsl": "Windows Subsystem for Linux",
    "maintenance": "Limpieza y mantenimiento del sistema",
    "help": "Ayuda y documentación",
    "utility": "Utilidades varias de shell",
    "modernized": "Comando con reemplazo moderno recomendado (Regla 4)",
}


def is_valid_tag(tag: str) -> bool:
    return tag in TAGS
