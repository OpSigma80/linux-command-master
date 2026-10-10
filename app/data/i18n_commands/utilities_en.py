"""Traducciones EN -- categoria "utilities" (Utilidades y Ayuda)."""

COMMAND_EN: dict[str, dict] = {
    "man": {
        "description": "Shows a command's full manual page.",
        "syntax": "man command",
        "examples": ["man ls", "man 5 crontab  # section 5: file formats"],
        "when_to_use": "Check the official, complete documentation of any command.",
    },
    "info": {
        "description": "Documentation system alternative to man, with hypertext navigation.",
        "syntax": "info command",
        "examples": ["info coreutils"],
        "when_to_use": "GNU command documentation with a more navigable format than man.",
    },
    "help": {
        "description": "Shows help for Bash's internal (builtin) commands.",
        "syntax": "help command",
        "examples": ["help cd", "help export"],
        "when_to_use": "Check help for commands that are part of the shell and have no man page of their own.",
    },
    "apropos": {
        "description": "Searches man pages for commands related to a keyword.",
        "syntax": "apropos word",
        "examples": ["apropos copy"],
        "when_to_use": "When you don't remember a command's exact name but know what it does.",
    },
    "history": {
        "description": "Shows the history of commands run in the session.",
        "examples": ["history", "history | grep docker", "!245  # re-run command 245"],
        "when_to_use": "Recall a previously run command without retyping it.",
    },
    "alias": {
        "description": "Creates a shortcut/abbreviation for a long command.",
        "syntax": 'alias name="command"',
        "examples": ['alias ll="ls -la"', 'alias gs="git status"'],
        "when_to_use": "Speed up frequent commands; usually defined in ~/.bashrc.",
    },
    "unalias": {
        "description": "Removes a previously defined alias.",
        "syntax": "unalias name",
        "examples": ["unalias ll"],
        "when_to_use": "Remove an alias from the current session.",
    },
    "clear": {
        "description": "Clears the terminal screen.",
        "when_to_use": "Visually clear the terminal without losing the history.",
    },
    "date": {
        "description": "Shows or sets the system date and time.",
        "syntax": 'date ["+format"]',
        "examples": ["date", 'date +"%Y-%m-%d"'],
        "when_to_use": "Get timestamps for logs, file names or scripts.",
    },
    "cal": {
        "description": "Shows a calendar in the terminal.",
        "syntax": "cal [month] [year]",
        "examples": ["cal", "cal 12 2026"],
        "when_to_use": "Quick date lookup without leaving the terminal.",
    },
    "watch": {
        "description": "Runs a command repeatedly at intervals, showing the updated output.",
        "syntax": "watch [-n seconds] command",
        "examples": ["watch -n 2 docker ps", "watch df -h"],
        "when_to_use": "Monitor a command's output live without extra scripting.",
        "options": ["-n (interval in seconds)"],
    },
    "yes": {
        "description": "Prints a string repeatedly until interrupted, useful to auto-answer prompts.",
        "syntax": "yes [string]",
        "examples": ["yes | command_that_asks_yes_no"],
        "when_to_use": "Automate affirmative answers to interactive commands in scripts.",
    },
    "seq": {
        "description": "Generates a sequence of numbers.",
        "syntax": "seq start [step] end",
        "examples": ["seq 1 10", "seq 0 2 20"],
        "when_to_use": "Generate numeric ranges for for-loops in scripts.",
    },
    "sleep": {
        "description": "Pauses execution for a given amount of time.",
        "syntax": "sleep time",
        "examples": ["sleep 5", "sleep 2m"],
        "when_to_use": "Wait between retries or steps in automation scripts.",
    },
    "printf": {
        "description": "Prints text with precise format control (more predictable than echo).",
        "syntax": 'printf "format" arguments',
        "examples": ['printf "Name: %s, Age: %d\\n" "Ana" 30'],
        "when_to_use": "Format output in scripts where echo isn't precise enough.",
    },
    "echo": {
        "description": "Prints text or the value of variables to the screen.",
        "syntax": "echo text",
        "examples": ['echo "Hello world"', 'echo "$VAR"'],
        "when_to_use": "Show messages or debug variable values in scripts.",
    },
}
