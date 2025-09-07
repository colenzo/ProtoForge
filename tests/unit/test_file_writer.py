import pytest
import os
from src.core.file_writer import write_code_to_files

@pytest.mark.asyncio
async def test_write_code_to_files_basic(tmp_path):
    base_path = tmp_path
    file_structure = {
        "app": ["main.py"]
    }
    code_content = """--- FILE: app/main.py ---
print("Hello, World!")
"""
    await write_code_to_files(base_path, file_structure, code_content)

    # Assertions
    assert (base_path / "app").is_dir()
    assert (base_path / "app" / "main.py").is_file()
    assert (base_path / "app" / "main.py").read_text() == 'print("Hello, World!")'

@pytest.mark.asyncio
async def test_write_code_to_files_multiple_files_and_dirs(tmp_path):
    base_path = tmp_path
    file_structure = {
        "src": ["app.py", "utils.py"],
        "tests": ["test_app.py"]
    }
    code_content = """--- FILE: src/app.py ---
def run():
    pass
--- FILE: src/utils.py ---
def helper():
    pass
--- FILE: tests/test_app.py ---
import pytest
"""
    await write_code_to_files(base_path, file_structure, code_content)

    # Assertions
    assert (base_path / "src").is_dir()
    assert (base_path / "tests").is_dir()
    assert (base_path / "src" / "app.py").is_file()
    assert (base_path / "src" / "utils.py").is_file()
    assert (base_path / "tests" / "test_app.py").is_file()

    assert (base_path / "src" / "app.py").read_text() == 'def run():\n    pass'
    assert (base_path / "src" / "utils.py").read_text() == 'def helper():\n    pass'
    assert (base_path / "tests" / "test_app.py").read_text() == 'import pytest'

@pytest.mark.asyncio
async def test_write_code_to_files_empty_structure(tmp_path):
    base_path = tmp_path
    file_structure = {}
    code_content = """--- FILE: app/main.py ---
print("Hello, World!")
"""
    await write_code_to_files(base_path, file_structure, code_content)
    # Assert that no directories or files were created
    assert not list(base_path.iterdir())

@pytest.mark.asyncio
async def test_write_code_to_files_content_not_found(tmp_path, capsys):
    base_path = tmp_path
    file_structure = {
        "app": ["main.py"]
    }
    code_content = """--- FILE: other/file.py ---
print("Something else")
""" # Content for main.py is missing
    await write_code_to_files(base_path, file_structure, code_content)

    # Assertions
    assert (base_path / "app").is_dir()
    assert not (base_path / "app" / "main.py").is_file() # File should not be created

    captured = capsys.readouterr()
    assert "Warning: Content for app/main.py not found in code_content. Skipping." in captured.out
