from app.data.models import Command, Level, Risk

COMMANDS: list[Command] = [
    Command(
        id="wsl-list", name="wsl --list", category="wsl", subcategory="management",
        description="Lista las distribuciones Linux instaladas en WSL (ejecutar desde PowerShell/CMD de Windows).",
        syntax="wsl --list [-v]",
        examples=["wsl --list -v"],
        when_to_use="Ver qué distros tienes instaladas y su versión de WSL (1 o 2).",
        options=["-v (verbose, muestra versión de WSL)"],
        related=["wsl-status"], tags=["wsl"], level=Level.BASICO,
    ),
    Command(
        id="wsl-status", name="wsl --status", category="wsl", subcategory="management",
        description="Muestra la configuración general de WSL (distro por defecto, versión).",
        syntax="wsl --status",
        examples=["wsl --status"],
        when_to_use="Diagnóstico rápido de la configuración global de WSL.",
        related=["wsl-list"], tags=["wsl"], level=Level.BASICO,
    ),
    Command(
        id="wsl-shutdown", name="wsl --shutdown", category="wsl", subcategory="management",
        description="Apaga por completo la máquina virtual de WSL (todas las distros).",
        syntax="wsl --shutdown",
        examples=["wsl --shutdown"],
        when_to_use="Liberar memoria RAM acaparada por WSL, o forzar un reinicio limpio tras cambiar .wslconfig.",
        related=["wsl-update"], tags=["wsl", "performance"], level=Level.INTERMEDIO,
    ),
    Command(
        id="wsl-update", name="wsl --update", category="wsl", subcategory="management",
        description="Actualiza el kernel de WSL a la última versión.",
        syntax="wsl --update",
        examples=["wsl --update"],
        when_to_use="Solucionar problemas de compatibilidad o aplicar mejoras de rendimiento del kernel de WSL.",
        related=["wsl-shutdown"], tags=["wsl"], level=Level.INTERMEDIO,
    ),
    Command(
        id="wsl-export", name="wsl --export", category="wsl", subcategory="management",
        description="Exporta una distro completa a un archivo .tar, útil como backup.",
        syntax="wsl --export Distro archivo.tar",
        examples=["wsl --export Debian debian_backup.tar"],
        when_to_use="Hacer backup de tu entorno WSL Debian completo antes de cambios grandes.",
        related=["wsl-import"], tags=["wsl", "maintenance"], level=Level.AVANZADO,
    ),
    Command(
        id="wsl-import", name="wsl --import", category="wsl", subcategory="management",
        description="Importa una distro desde un archivo .tar exportado previamente.",
        syntax="wsl --import NuevaDistro C:\\ruta\\destino archivo.tar",
        examples=["wsl --import DebianBackup C:\\WSL\\DebianBackup debian_backup.tar"],
        when_to_use="Restaurar un backup de WSL o clonar tu entorno en otra ubicación.",
        related=["wsl-export"], tags=["wsl"], level=Level.AVANZADO,
    ),
    Command(
        id="wslconfig", name=".wslconfig", category="wsl", subcategory="performance",
        description="Archivo de configuración global de WSL2 en Windows (%UserProfile%\\.wslconfig) para limitar RAM/CPU.",
        syntax="[wsl2]\\nmemory=8GB\\nprocessors=4",
        examples=["[wsl2]", "memory=8GB", "processors=4", "swap=2GB"],
        when_to_use=(
            "Con 16GB de RAM en tu laptop, limitar la memoria de WSL (ej: memory=8GB) "
            "evita que consuma toda la RAM disponible para Windows."
        ),
        related=["wsl-shutdown"], tags=["wsl", "performance"], level=Level.AVANZADO,
    ),
    Command(
        id="mnt-c", name="/mnt/c (integración Windows)", category="wsl", subcategory="performance",
        description="Punto de montaje donde WSL expone el sistema de archivos de Windows.",
        syntax="/mnt/c/Users/tu_usuario/...",
        examples=["cd /mnt/c/Users/tu_usuario/Documents"],
        when_to_use="Acceder a archivos de Windows desde Debian; evita trabajar proyectos pesados directamente ahí por rendimiento de I/O.",
        precautions="El I/O a través de /mnt/c es notablemente más lento que trabajar en el filesystem nativo de WSL (~/).",
        related=["wslconfig"], tags=["wsl", "performance", "storage"], level=Level.INTERMEDIO,
    ),
]
