"""Traducciones EN -- categoria "compression" (Compresion y Archivos)."""

COMMAND_EN: dict[str, dict] = {
    "tar": {
        "description": "Packages (and optionally compresses) files and directories into a single file.",
        "syntax": "tar [options] archive.tar target",
        "examples": [
            "tar -cvf archive.tar folder/         # package",
            "tar -xvf archive.tar                 # extract",
            "tar -czvf archive.tar.gz folder/      # package + gzip",
            "tar -xzvf archive.tar.gz              # extract .tar.gz",
        ],
        "when_to_use": "The standard Linux format to package backups, releases, or transfer file trees.",
        "options": ["-c (create)", "-x (extract)", "-v (verbose)", "-f (file)", "-z (gzip)", "-j (bzip2)", "-J (xz)"],
    },
    "gzip": {
        "name": "gzip / gunzip",
        "description": "Compresses or decompresses a single file with the gzip algorithm (.gz).",
        "syntax": "gzip file / gunzip file.gz",
        "examples": ["gzip file.txt", "gunzip file.txt.gz"],
        "when_to_use": "Quick compression of a single file; for directories, combine it with tar (tar.gz).",
    },
    "zip": {
        "name": "zip / unzip",
        "description": "Compresses or decompresses files in .zip format, compatible with Windows/macOS.",
        "syntax": "zip -r archive.zip folder/ / unzip archive.zip",
        "examples": ["zip -r project.zip project/", "unzip project.zip"],
        "when_to_use": "When the compressed file needs to be shared with Windows/macOS users.",
        "options": ["-r (recursive)"],
    },
    "bzip2": {
        "description": "Compressor with a better ratio than gzip but slower (.bz2).",
        "syntax": "bzip2 file",
        "examples": ["bzip2 file.txt", "tar -xjvf archive.tar.bz2"],
        "when_to_use": "When final size matters more than compression speed.",
    },
    "xz": {
        "description": "Compressor with the best compression ratio, slower than gzip and bzip2 (.xz).",
        "syntax": "xz file",
        "examples": ["xz file.txt", "tar -xJvf archive.tar.xz"],
        "when_to_use": "Backups or releases where minimizing file size is the priority.",
    },
    "7z": {
        "name": "7z (p7zip)",
        "description": "High-ratio compressor with its own format (.7z), requires installing p7zip.",
        "syntax": "7z a archive.7z folder/",
        "examples": ["7z a backup.7z folder/", "7z x backup.7z"],
        "when_to_use": "When you need maximum compression or compatibility with Windows .7z files.",
    },
}
