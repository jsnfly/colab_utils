from pathlib import Path
import shutil

def copy_file(source, destination):
    source = Path(source)
    destination = Path(destination)
    dest_dir = destination if destination.suffix == '' else destination.parent
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(str(source), str(destination))