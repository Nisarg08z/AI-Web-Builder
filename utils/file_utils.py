import os
from pathlib import Path
import shutil

def save_file(path: str, content: str):
    filepath = Path(path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding='utf-8')

def zip_project(project_path: str, output_dir: str):
    folder_name = os.path.basename(project_path)
    zip_path = os.path.join(output_dir, folder_name)
    shutil.make_archive(zip_path, 'zip', project_path)
    return f"{zip_path}.zip"

def delete_project(project_name: str):
    folder = os.path.join("generated", project_name)
    try:
        if os.path.exists(folder) and os.path.isdir(folder):
            shutil.rmtree(folder)
            return True
        return False
    except Exception as e:
        print(f"Error deleting project folder: {e}")
        return False
