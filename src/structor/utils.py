import os
from pathlib import Path


def create_dirs_if_not_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def create_file_if_not_exists(path: str):
    fle = Path(path)
    fle.touch(exist_ok=True)


def struct_param(index: int) -> str:
    return f"**{index + 1}"
