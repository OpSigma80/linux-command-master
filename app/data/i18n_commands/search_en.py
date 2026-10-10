"""Traducciones EN -- categoria "search" (Busqueda)."""

COMMAND_EN: dict[str, dict] = {
    "find": {
        "description": "Searches files and directories by walking the directory tree in real time, with multiple filters.",
        "syntax": "find [path] [criteria] [action]",
        "examples": [
            "find . -name '*.py'",
            "find /var/log -mtime -7",
            "find . -type f -size +10M",
            "find . -name '*.tmp' -exec rm {} \\;",
        ],
        "when_to_use": "Complex searches by name, type, size, date, or to run actions on the results.",
        "precautions": "find + -exec rm is powerful but dangerous: test first with -exec echo {} \\;",
    },
    "locate": {
        "description": "Searches files by name using a precomputed index (much faster than find, but may be outdated).",
        "syntax": "locate pattern",
        "examples": ["locate file.conf", "sudo updatedb  # update the index"],
        "when_to_use": "Fast system-wide name searches when speed matters more than freshness.",
    },
    "rg": {
        "name": "rg (ripgrep)",
        "description": "Text search tool, similar to grep but much faster and automatically excludes .gitignore.",
        "syntax": "rg pattern [path]",
        "examples": ["rg 'TODO' ./src", "rg -i 'error'"],
        "when_to_use": "Text searches in large codebases, faster than grep -R.",
    },
    "which": {
        "description": "Shows the path of the executable that would run for a given command.",
        "syntax": "which command",
        "examples": ["which python3", "which docker"],
        "when_to_use": "Verify exactly which binary would run (useful with multiple versions installed).",
    },
    "whereis": {
        "description": "Locates a command's binary, source code and manual page.",
        "syntax": "whereis command",
        "examples": ["whereis grep"],
        "when_to_use": "When you also need the manual's location, not just the binary.",
    },
    "type": {
        "description": "Shows whether a name is an alias, function, shell builtin, or executable.",
        "syntax": "type command",
        "examples": ["type cd", "type ls"],
        "when_to_use": "Tell whether a command is a bash builtin or an external binary.",
    },
    "command": {
        "description": "Runs a command ignoring functions or aliases with the same name.",
        "syntax": "command command",
        "examples": ["command ls  # ignores ls alias"],
        "when_to_use": "Inside scripts, to prevent an alias from overriding the expected behavior.",
    },
}
