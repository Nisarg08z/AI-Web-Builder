import os
from pathlib import Path
import shutil
import tempfile

def save_file(path: str, content: str):
    filepath = Path(f"generated/{path}")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding='utf-8')

def zip_project(folder="generated", output_name="generated_site", output_dir=None):
    output_dir = output_dir or folder
    output_path = os.path.join(output_dir, output_name)
    shutil.make_archive(output_path, 'zip', folder)
    return f"{output_path}.zip"

def delete_file(path):
    try:
        os.remove(path)
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

def delete_generated_folder(folder="generated"):
    try:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            return True
        return False
    except Exception as e:
        print(f"Error deleting generated folder: {e}")
        return False
