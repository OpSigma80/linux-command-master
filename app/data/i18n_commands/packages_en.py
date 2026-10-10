"""Traducciones EN -- categoria "packages" (Gestion de Paquetes)."""

COMMAND_EN: dict[str, dict] = {
    "apt": {
        "description": "Modern, user-friendly package manager for Debian/Ubuntu/WSL.",
        "syntax": "sudo apt command [package]",
        "examples": [
            "sudo apt update",
            "sudo apt upgrade",
            "sudo apt install nginx",
            "sudo apt remove nginx",
            "sudo apt search docker",
        ],
        "when_to_use": "Install, update or remove software on Debian/Ubuntu/WSL Debian.",
    },
    "apt-get": {
        "description": "Classic version of apt, more script-oriented (more stable/parseable output).",
        "syntax": "sudo apt-get command [package]",
        "examples": ["sudo apt-get update", "sudo apt-get install -y package"],
        "when_to_use": "Inside scripts or Dockerfiles, where apt-get's stable output is preferred.",
    },
    "apt-cache": {
        "description": "Queries information about available packages without installing them.",
        "syntax": "apt-cache command package",
        "examples": ["apt-cache search docker", "apt-cache show nginx"],
        "when_to_use": "Research a package (dependencies, description) before installing it.",
    },
    "dpkg": {
        "description": "Low-level package manager for .deb files (apt works on top of dpkg).",
        "syntax": "sudo dpkg [options] package.deb",
        "examples": ["sudo dpkg -i package.deb", "dpkg -l | grep nginx"],
        "when_to_use": "Install a manually downloaded .deb or list installed packages.",
        "options": ["-i (install)", "-l (list)", "-r (remove)"],
    },
    "snap": {
        "description": "Universal package manager (snaps), independent of the distro version.",
        "syntax": "sudo snap command package",
        "examples": ["sudo snap install code --classic", "snap list"],
        "when_to_use": "Install software distributed as a snap (e.g: some desktop apps).",
    },
    "pip": {
        "description": "Python package manager (libraries for the active interpreter).",
        "syntax": "pip install package",
        "when_to_use": "Install Python dependencies inside a virtual environment or Conda.",
        "precautions": "Avoid using 'sudo pip install' system-wide: use virtual environments or Conda instead.",
    },
    "conda": {
        "description": "Anaconda's environment and package manager, handles both Python and binary dependencies.",
        "syntax": "conda command",
        "examples": [
            "conda create -n project python=3.11",
            "conda activate project",
            "conda install numpy pandas",
            "conda env list",
        ],
        "when_to_use": "Create isolated per-project environments (recommended with your Anaconda install).",
    },
    "jupyter": {
        "description": "Launches the Jupyter Notebook/Lab server for interactive Python development.",
        "syntax": "jupyter notebook / jupyter lab",
        "when_to_use": "Data analysis or interactive prototyping inside a Conda environment.",
    },
}
