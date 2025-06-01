import os
from pathlib import Path
import shutil

def save_file(path: str, content: str):
    filepath = Path(path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding='utf-8')

def zip_project(project_folder: str, output_dir: str = "generated"):
    folder_path = os.path.join(output_dir, project_folder)
    output_path = os.path.join(output_dir, project_folder)
    shutil.make_archive(output_path, 'zip', folder_path)
    return f"{output_path}.zip"

def delete_generated_content(folder: str = "generated"):
    try:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        return True
    except Exception as e:
        print(f"Error clearing generated folder: {e}")
        return False
