import os
from pathlib import Path
import shutil

def save_file(path: str, content: str):
    filepath = Path(path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    # Write content preserving formatting (no modifications)
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
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error clearing generated folder: {e}")
        return False
