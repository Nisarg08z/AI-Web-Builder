import os
from pathlib import Path
import shutil

def save_file(path: str, content: str):
    filepath = Path(f"generated/{path}")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding='utf-8')

def zip_project(folder="generated", output_name="generated_site"):
    shutil.make_archive(output_name, 'zip', folder)
    return f"{output_name}.zip"
