"""Traducciones EN -- categoria "system" (Informacion del Sistema)."""

COMMAND_EN: dict[str, dict] = {
    "uname": {
        "description": "Shows kernel information and system architecture.",
        "syntax": "uname [-a]",
        "when_to_use": "Identify kernel version and architecture, useful when debugging compatibility.",
        "options": ["-a (all info)", "-r (kernel version)"],
    },
    "lscpu": {
        "description": "Shows detailed CPU information (cores, architecture, cache).",
        "when_to_use": "Know available CPU capabilities, for example before configuring Docker/WSL.",
    },
    "lsblk": {
        "description": "Lists the system's block devices (disks and partitions).",
        "examples": ["lsblk", "lsblk -f  # with filesystem"],
        "when_to_use": "View available disks and partitions before mounting or partitioning.",
    },
    "lsusb": {
        "description": "Lists USB devices connected to the system.",
        "when_to_use": "Diagnose whether a USB device is recognized by the system.",
    },
    "lspci": {
        "description": "Lists devices connected to the PCI bus (GPU, network, etc).",
        "examples": ["lspci", "lspci -k  # with driver in use"],
        "when_to_use": "Identify internal hardware like network cards or GPUs.",
    },
    "dmesg": {
        "description": "Shows the kernel buffer messages (boot, hardware, errors).",
        "syntax": "dmesg [-T]",
        "examples": ["dmesg | tail -50", "dmesg -T | grep -i error"],
        "when_to_use": "Diagnose hardware, driver, or kernel-level errors.",
        "options": ["-T (human-readable timestamps)"],
    },
    "hostname": {
        "description": "Shows or sets the system's hostname.",
        "syntax": "hostname [new_name]",
        "when_to_use": "Quickly check the machine's name.",
    },
    "hostnamectl": {
        "description": "Shows or configures the hostname along with system info (systemd).",
        "syntax": "hostnamectl [command]",
        "examples": ["hostnamectl", "sudo hostnamectl set-hostname new-name"],
        "when_to_use": "Check hostname, kernel, architecture and virtualization in a single command.",
    },
    "lsb_release": {
        "description": "Shows information about the installed Linux distribution (version, codename).",
        "syntax": "lsb_release -a",
        "when_to_use": "Confirm the exact Debian/Ubuntu version before installing packages.",
    },
    "df": {
        "description": "Shows used and available disk space per filesystem.",
        "syntax": "df [-h]",
        "when_to_use": "Check free disk space before installing software or running backups.",
        "options": ["-h (human-readable)"],
    },
    "du": {
        "description": "Shows the disk space used by files or directories.",
        "syntax": "du [-sh] path",
        "examples": ["du -sh folder/", "du -h --max-depth=1 ."],
        "when_to_use": "Find which folders are taking up the most space.",
        "options": ["-s (summary)", "-h (human-readable)"],
    },
    "fdisk": {
        "description": "Interactive tool to view and modify a disk's partition table.",
        "syntax": "sudo fdisk -l / sudo fdisk /dev/sdX",
        "when_to_use": "View or create partitions on a disk (MBR/GPT).",
        "precautions": "Modifying partitions incorrectly can destroy all data on the disk.",
    },
    "parted": {
        "description": "Tool to create, resize or delete partitions, with GPT support.",
        "syntax": "sudo parted /dev/sdX",
        "examples": ["sudo parted -l"],
        "when_to_use": "Manage partitions on large disks (>2TB) that require GPT.",
        "precautions": "Mistakes here can cause total data loss on the disk.",
    },
    "blkid": {
        "description": "Shows block device attributes: UUID, filesystem type, label.",
        "syntax": "sudo blkid",
        "when_to_use": "Get a partition's UUID to configure /etc/fstab.",
    },
    "mkfs": {
        "description": "Creates (formats) a filesystem on a partition or device.",
        "syntax": "sudo mkfs.type /dev/sdXN",
        "examples": ["sudo mkfs.ext4 /dev/sdb1"],
        "when_to_use": "Format a new partition before mounting it.",
        "precautions": "Formatting a device ERASES all existing data irreversibly. Triple-check the device name.",
    },
    "env": {
        "description": "Shows all environment variables or runs a command with a modified environment.",
        "examples": ["env", "env VAR=value command"],
        "when_to_use": "View the full environment, or inject temporary variables into a single command.",
    },
    "printenv": {
        "description": "Shows the value of one or all environment variables.",
        "syntax": "printenv [VAR]",
        "when_to_use": "Check the value of a specific environment variable.",
    },
}
