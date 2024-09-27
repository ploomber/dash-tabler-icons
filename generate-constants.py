from pathlib import Path
from glob import glob
import os
import tempfile
import shutil
from pathlib import Path
import subprocess
from contextlib import contextmanager
from typing import List
from pathlib import Path

PATH_TO_HERE = Path(__file__).parent

PATH_TO_ICONS_PY = PATH_TO_HERE / "dash_tabler_icons" / "icons.py"


def generate_icon_enum(icon_names: List[str]) -> str:
    enum_content = """from enum import Enum

class IconName(str, Enum):
    def __new__(cls, value):
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"IconName.{self.name}"

"""
    for icon_name in icon_names:
        enum_content += f"    Icon{icon_name} = 'Icon{icon_name}'\n"
    return enum_content


@contextmanager
def clone_repo(github_url: str):
    original_dir = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        try:
            # Clone the repository with depth 1 to get only the latest commit
            subprocess.run(
                ["git", "clone", "--depth", "1", github_url, str(tmp_path)], check=True
            )
            os.chdir(tmp_path)
            yield tmp_path
        finally:
            os.chdir(original_dir)
            # Cleanup is handled automatically by tempfile.TemporaryDirectory


def to_pascal_case(string: str) -> str:
    # Split the string by non-alphanumeric characters
    words = "".join(char if char.isalnum() else " " for char in string).split()
    # Capitalize the first letter of each word and join them
    return "".join(word.capitalize() for word in words)


with clone_repo("https://github.com/tabler/tabler-icons"):
    # Get a list of files in icons/filled using iglob
    icon_files_filled = glob("icons/filled/*.svg")
    icon_files_outline = glob("icons/outline/*.svg")

    # Convert file paths to icon names
    icon_names_filled = [
        to_pascal_case(Path(file).stem) + "Filled" for file in icon_files_filled
    ]
    icon_names_outline = [
        to_pascal_case(Path(file).stem) for file in icon_files_outline
    ]

    enum_string = generate_icon_enum(icon_names_filled + icon_names_outline)
    Path(PATH_TO_ICONS_PY).write_text(enum_string)
