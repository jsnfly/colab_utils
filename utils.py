from pathlib import Path
import shutil

def copy_file(source, destination):
    source = Path(source)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy(str(source), str(destination))