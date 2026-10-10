"""
Traducciones EN — categoría "files" (Navegación y Gestión de Archivos).

Primera categoría traducida, como prueba del mecanismo de i18n antes de
continuar con las 15 restantes (Fase B). Estructura: un dict por comando,
solo con los campos de texto libre (los campos estructurales — category,
subcategory, tags, level, risk, related — se mantienen desde la ficha ES,
no se duplican).
"""

COMMAND_EN: dict[str, dict] = {
    "pwd": {
        "description": "Shows the absolute path of the current directory.",
        "when_to_use": "To confirm where you are before running relative commands.",
    },
    "cd": {
        "description": "Changes the current working directory.",
        "syntax": "cd [path]",
        "when_to_use": "Basic navigation between directories.",
        "options": ["~ (home)", "- (previous directory)", ".. (parent)"],
    },
    "ls": {
        "description": "Lists the contents of a directory.",
        "syntax": "ls [options] [path]",
        "when_to_use": "Inspect files, permissions and sizes of a directory.",
        "options": ["-l (detail)", "-a (hidden)", "-h (human-readable)", "-R (recursive)"],
    },
    "tree": {
        "description": "Shows the directory structure as a tree.",
        "syntax": "tree [options] [path]",
        "when_to_use": "Quickly visualize the hierarchy of a project.",
    },
    "mkdir": {
        "description": "Creates one or more directories.",
        "syntax": "mkdir [-p] directory",
        "when_to_use": "Create folder structures, with -p for nested paths.",
        "options": ["-p (creates parents if missing)"],
    },
    "rmdir": {
        "description": "Removes empty directories.",
        "syntax": "rmdir directory",
        "when_to_use": "Safely delete empty directories (fails if they have content).",
    },
    "touch": {
        "description": "Creates empty files or updates their modification time.",
        "syntax": "touch file",
        "when_to_use": "Quickly create files or force timestamps in scripts.",
    },
    "cp": {
        "description": "Copies files or directories.",
        "syntax": "cp [options] source destination",
        "when_to_use": "Duplicate files or entire directories.",
        "options": ["-r (recursive)", "-v (verbose)", "-i (confirm overwrite)"],
    },
    "mv": {
        "description": "Moves or renames files and directories.",
        "syntax": "mv source destination",
        "when_to_use": "Rename files or relocate them.",
    },
    "rm": {
        "description": "Permanently deletes files or directories (no recycle bin).",
        "syntax": "rm [options] file",
        "when_to_use": "Definitive deletion of files or directories.",
        "options": ["-r (recursive)", "-f (force, no confirmation)"],
        "precautions": (
            "rm -rf has no recycle bin: ALWAYS verify the path before running it, "
            "especially with variable paths in scripts."
        ),
    },
    "ln": {
        "description": "Creates links (hard links or symlinks) between files.",
        "syntax": "ln [-s] source link",
        "when_to_use": "Create shortcuts (-s) or hard links to files.",
        "options": ["-s (symbolic link)"],
    },
    "readlink": {
        "description": "Shows where a symbolic link points to.",
        "syntax": "readlink [-f] link",
        "when_to_use": "Resolve the real path behind a symlink in scripts.",
    },
    "realpath": {
        "description": "Shows the canonical absolute path of a file.",
        "syntax": "realpath file",
        "when_to_use": "Get reliable absolute paths inside scripts.",
    },
    "file": {
        "description": "Determines a file's type by analyzing its content.",
        "syntax": "file file",
        "when_to_use": "Identify a file's real type without trusting the extension.",
    },
    "stat": {
        "description": "Shows detailed metadata of a file (size, permissions, dates, inode).",
        "syntax": "stat file",
        "when_to_use": "Audit permissions, timestamps or inode of a file.",
    },
    "basename": {
        "description": "Extracts the file name from a full path.",
        "syntax": "basename path",
        "when_to_use": "Inside scripts, to get just the file name.",
    },
    "dirname": {
        "description": "Extracts the containing directory from a full path.",
        "syntax": "dirname path",
        "when_to_use": "Inside scripts, to get the containing folder.",
    },
}
