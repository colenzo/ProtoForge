import os
from typing import Dict, List

async def write_code_to_files(base_path: str, file_structure: Dict[str, List[str]], code_content: str):
    """Writes code content to files based on the provided file structure."""
    print(f"[FILE_WRITER] Writing code to files in base path: {base_path}")
    
    # For simplicity, we'll just write the entire code_content to the first file in the structure
    # In a real scenario, the code_content would be parsed and distributed to multiple files
    
    if not file_structure:
        print("[FILE_WRITER] No file structure provided. Skipping file writing.")
        return

    # Get the first directory and file from the structure
    first_dir = list(file_structure.keys())[0]
    if not file_structure[first_dir]:
        print(f"[FILE_WRITER] No files specified for directory {first_dir}. Skipping file writing.")
        return
    first_file = file_structure[first_dir][0]

    target_dir = os.path.join(base_path, first_dir)
    os.makedirs(target_dir, exist_ok=True)
    target_file_path = os.path.join(target_dir, first_file)

    try:
        with open(target_file_path, "w") as f:
            f.write(code_content)
        print(f"[FILE_WRITER] Successfully wrote code to: {target_file_path}")
    except Exception as e:
        print(f"[FILE_WRITER] Error writing code to {target_file_path}: {e}")
