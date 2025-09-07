import os
from typing import Dict, List
import re

async def write_code_to_files(base_path: str, file_structure: Dict[str, List[str]], code_content: str):
    """Writes code content to files based on the provided file structure and parsed code_content."""
    print(f"[FILE_WRITER] Writing code to files in base path: {base_path}")
    
    if not file_structure:
        print("[FILE_WRITER] No file structure provided. Skipping file writing.")
        return

    # Parse the code_content into individual file contents
    files_data = {}
    current_file_path = None
    current_file_content = []

    # Split content by the file delimiter
    sections = re.split(r'^--- FILE: (.*?) ---', code_content, flags=re.MULTILINE)
    
    # The first element is usually empty or content before the first file
    # Iterate through pairs of (filename, content)
    for i in range(1, len(sections), 2):
        file_path_in_content = sections[i].strip()
        content = sections[i+1]
        files_data[file_path_in_content] = content.strip()

    # Write each file
    for dir_name, file_list in file_structure.items():
        target_dir = os.path.join(base_path, dir_name)
        os.makedirs(target_dir, exist_ok=True)

        for file_name in file_list:
            full_path_in_content = os.path.join(dir_name, file_name).replace("\\\\", "/") # Normalize path for lookup
            
            if full_path_in_content in files_data:
                target_file_path = os.path.join(target_dir, file_name)
                try:
                    with open(target_file_path, "w") as f:
                        f.write(files_data[full_path_in_content])
                    print(f"[FILE_WRITER] Successfully wrote code to: {target_file_path}")
                except Exception as e:
                    print(f"[FILE_WRITER] Error writing code to {target_file_path}: {e}")
            else:
                print(f"[FILE_WRITER] Warning: Content for {full_path_in_content} not found in code_content. Skipping.")