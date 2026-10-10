from app.data.models import Command, Level, Risk

COMMANDS: list[Command] = [
    Command(
        id="tar", name="tar", category="compression", subcategory="archive",
        description="Empaqueta (y opcionalmente comprime) archivos y directorios en un solo archivo.",
        syntax="tar [opciones] archivo.tar objetivo",
        examples=[
            "tar -cvf archivo.tar carpeta/         # empaquetar",
            "tar -xvf archivo.tar                  # extraer",
            "tar -czvf archivo.tar.gz carpeta/      # empaquetar + gzip",
            "tar -xzvf archivo.tar.gz               # extraer .tar.gz",
        ],
        when_to_use="Formato estándar en Linux para empaquetar backups, releases o transferir árboles de archivos.",
        options=["-c (crear)", "-x (extraer)", "-v (verbose)", "-f (archivo)", "-z (gzip)", "-j (bzip2)", "-J (xz)"],
        related=["gzip", "zip"], tags=["compression"], level=Level.INTERMEDIO,
    ),
    Command(
        id="gzip", name="gzip / gunzip", category="compression", subcategory="archive",
        description="Comprime o descomprime un único archivo con el algoritmo gzip (.gz).",
        syntax="gzip archivo / gunzip archivo.gz",
        examples=["gzip archivo.txt", "gunzip archivo.txt.gz"],
        when_to_use="Compresión rápida de un solo archivo; para directorios combínalo con tar (tar.gz).",
        related=["tar", "bzip2"], tags=["compression"], level=Level.BASICO,
    ),
    Command(
        id="zip", name="zip / unzip", category="compression", subcategory="archive",
        description="Comprime o descomprime archivos en formato .zip, compatible con Windows/macOS.",
        syntax="zip -r archivo.zip carpeta/ / unzip archivo.zip",
        examples=["zip -r proyecto.zip proyecto/", "unzip proyecto.zip"],
        when_to_use="Cuando el archivo comprimido debe compartirse con usuarios de Windows/macOS.",
        options=["-r (recursivo)"],
        related=["tar"], tags=["compression"], level=Level.BASICO,
    ),
    Command(
        id="bzip2", name="bzip2", category="compression", subcategory="archive",
        description="Compresor con mejor ratio que gzip pero más lento (.bz2).",
        syntax="bzip2 archivo",
        examples=["bzip2 archivo.txt", "tar -xjvf archivo.tar.bz2"],
        when_to_use="Cuando el tamaño final importa más que la velocidad de compresión.",
        related=["gzip", "xz"], tags=["compression"], level=Level.INTERMEDIO,
    ),
    Command(
        id="xz", name="xz", category="compression", subcategory="archive",
        description="Compresor con la mejor ratio de compresión, más lento que gzip y bzip2 (.xz).",
        syntax="xz archivo",
        examples=["xz archivo.txt", "tar -xJvf archivo.tar.xz"],
        when_to_use="Backups o releases donde se prioriza el tamaño mínimo del archivo.",
        related=["bzip2", "gzip"], tags=["compression"], level=Level.INTERMEDIO,
    ),
    Command(
        id="7z", name="7z (p7zip)", category="compression", subcategory="archive",
        description="Compresor de alta ratio con formato propio (.7z), requiere instalar p7zip.",
        syntax="7z a archivo.7z carpeta/",
        examples=["7z a backup.7z carpeta/", "7z x backup.7z"],
        when_to_use="Cuando necesitas máxima compresión o compatibilidad con archivos .7z de Windows.",
        related=["zip", "xz"], tags=["compression"], level=Level.INTERMEDIO,
    ),
]
