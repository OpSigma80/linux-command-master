"""Traducciones EN -- categoria "processes" (Procesos y Rendimiento)."""

COMMAND_EN: dict[str, dict] = {
    "ps": {
        "description": "Shows a snapshot of currently running processes.",
        "syntax": "ps [options]",
        "when_to_use": "See active processes at a given moment (not in real time).",
        "options": ["aux (all, BSD format)", "-ef (all, UNIX format)"],
    },
    "top": {
        "description": "Real-time process monitor, shows CPU and memory usage.",
        "when_to_use": "Diagnose which process is consuming resources live.",
        "options": ["M (sort by memory)", "P (sort by CPU)", "k (kill process)"],
    },
    "htop": {
        "description": "Interactive, visual version of top, with colors and keyboard/mouse navigation.",
        "when_to_use": "Same as top but with a friendlier interface (requires separate install).",
    },
    "pgrep": {
        "description": "Finds PIDs of processes matching a name or pattern.",
        "syntax": "pgrep pattern",
        "examples": ["pgrep python", "pgrep -f 'script.py'"],
        "when_to_use": "Get a process's PID by name, useful in scripts.",
    },
    "pkill": {
        "description": "Sends a signal (SIGTERM by default) to processes matching a name.",
        "syntax": "pkill pattern",
        "when_to_use": "Terminate processes by name without manually looking up the PID.",
        "precautions": "pkill without a precise filter can kill unintended processes with similar names.",
    },
    "kill": {
        "description": "Sends a signal to a specific process by its PID.",
        "syntax": "kill [-signal] PID",
        "when_to_use": "Terminate a specific process; -15 (TERM) is the polite shutdown, -9 (KILL) is forced.",
        "options": ["-15 (TERM, default)", "-9 (KILL, forced)"],
        "precautions": "kill -9 doesn't let the process release resources or save state; use it as a last resort.",
    },
    "killall": {
        "description": "Sends a signal to every process that exactly matches a name.",
        "syntax": "killall name",
        "when_to_use": "Terminate every instance of the same program.",
        "precautions": "Affects ALL processes with that exact name, including other users' if you have permission; verify it's what you want before running.",
    },
    "nice": {
        "description": "Starts a process with a given CPU priority.",
        "syntax": "nice -n value command",
        "when_to_use": "Run heavy tasks without hogging the CPU (higher values = lower priority).",
    },
    "renice": {
        "description": "Changes the priority of a process that's already running.",
        "syntax": "renice value -p PID",
        "when_to_use": "Adjust an active process's priority without restarting it.",
    },
    "jobs": {
        "description": "Lists the current session's background or foreground jobs.",
        "when_to_use": "See which processes launched with & are still active in the current terminal.",
    },
    "bg": {
        "description": "Resumes a stopped job and sends it to the background.",
        "syntax": "bg [%job]",
        "when_to_use": "Continue a process paused with Ctrl+Z in the background.",
    },
    "fg": {
        "description": "Brings a background job to the foreground.",
        "syntax": "fg [%job]",
        "when_to_use": "Regain interactive control of a background process.",
    },
    "nohup": {
        "description": "Runs a command immune to the HUP signal, so it keeps running after closing the terminal.",
        "syntax": "nohup command &",
        "examples": ["nohup ./script.sh &", "nohup python app.py > output.log 2>&1 &"],
        "when_to_use": "Keep long-running processes alive after closing an SSH session.",
    },
    "time": {
        "description": "Measures how long a command takes to run.",
        "syntax": "time command",
        "examples": ["time ./script.sh"],
        "when_to_use": "Measure a command's or script's performance.",
    },
    "uptime": {
        "description": "Shows how long the system has been running and the load average.",
        "when_to_use": "Quick diagnosis of system load.",
    },
    "free": {
        "description": "Shows the system's RAM and swap usage.",
        "syntax": "free [-h]",
        "when_to_use": "Diagnose memory usage in real time.",
        "options": ["-h (human-readable)"],
    },
    "vmstat": {
        "description": "Virtual memory, process, CPU and I/O statistics over intervals.",
        "syntax": "vmstat [interval] [count]",
        "when_to_use": "More detailed performance diagnosis than top, useful on servers.",
    },
    "iostat": {
        "description": "Shows CPU usage and disk I/O statistics.",
        "syntax": "iostat [interval]",
        "when_to_use": "Diagnose disk bottlenecks on servers.",
    },
}
