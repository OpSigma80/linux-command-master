"""Traducciones EN -- categoria "admin" (Administracion del Sistema)."""

COMMAND_EN: dict[str, dict] = {
    "systemctl": {
        "description": "Controls services and units managed by systemd.",
        "syntax": "systemctl [command] service",
        "when_to_use": "Start, stop, enable at boot, or check a service's status.",
    },
    "service": {
        "description": "Classic (pre-systemd) command to manage services; on modern distros it's a wrapper around systemctl.",
        "syntax": "service name command",
        "examples": ["sudo service nginx status"],
        "when_to_use": "Compatibility with older scripts; on newer systems prefer systemctl.",
    },
    "journalctl": {
        "description": "Queries systemd's centralized logs (the journal).",
        "syntax": "journalctl [options]",
        "examples": [
            "journalctl -u nginx",
            "journalctl -f            # follow live",
            "journalctl --since today",
            "sudo journalctl --vacuum-time=7d",
        ],
        "when_to_use": "Debug why a service failed, or review system logs in general.",
        "options": ["-u (unit/service)", "-f (follow live)", "--since", "--vacuum-time/--vacuum-size"],
        "precautions": "--vacuum-time/--vacuum-size permanently deletes old logs.",
    },
    "shutdown": {
        "description": "Shuts down or reboots the system on a schedule.",
        "syntax": "sudo shutdown [options] [time]",
        "examples": ["sudo shutdown now", "sudo shutdown -r +10  # reboot in 10 min"],
        "when_to_use": "Shut down/reboot in a controlled way, notifying other users.",
        "options": ["-r (reboot)", "-h (halt)", "now / +minutes"],
        "precautions": "Shuts down or reboots the system for all users and active processes; confirm there's no unsaved work.",
    },
    "reboot": {
        "description": "Reboots the system immediately.",
        "syntax": "sudo reboot",
        "examples": ["sudo reboot"],
        "when_to_use": "Direct reboot with no delay, typical after kernel updates.",
        "precautions": "Reboots immediately with no prior warning to other users, and no time to save ongoing work.",
    },
    "poweroff": {
        "description": "Shuts down the system immediately.",
        "syntax": "sudo poweroff",
        "examples": ["sudo poweroff"],
        "when_to_use": "Direct shutdown of the machine or server.",
        "precautions": "Shuts down immediately with no prior warning; on a remote server it can leave you without access until a manual restart.",
    },
    "mount": {
        "description": "Mounts a filesystem at a mount point.",
        "syntax": "sudo mount /dev/device /mount/point",
        "examples": ["sudo mount /dev/sdb1 /mnt/data"],
        "when_to_use": "Make an external partition or device accessible.",
    },
    "umount": {
        "description": "Unmounts a previously mounted filesystem.",
        "syntax": "sudo umount /mount/point",
        "examples": ["sudo umount /mnt/data"],
        "when_to_use": "Before physically disconnecting an external device.",
    },
    "lsmod": {
        "description": "Lists currently loaded kernel modules.",
        "when_to_use": "Diagnose active drivers or kernel modules.",
    },
    "modprobe": {
        "description": "Loads or unloads kernel modules.",
        "syntax": "sudo modprobe [-r] module",
        "examples": ["sudo modprobe nvidia"],
        "when_to_use": "Manually enable a kernel driver/module.",
    },
    "crontab": {
        "description": "Manages periodic scheduled tasks per user (cron jobs).",
        "examples": ["crontab -e", "crontab -l", "0 3 * * * /home/user/backup.sh"],
        "when_to_use": "Automate recurring tasks: backups, cleanups, reports.",
        "options": ["-e (edit)", "-l (list)", "-r (remove all)"],
    },
    "systemd-analyze": {
        "description": "Analyzes system and service boot time.",
        "syntax": "systemd-analyze [command]",
        "when_to_use": "Diagnose which service is slowing down system boot.",
    },
}
