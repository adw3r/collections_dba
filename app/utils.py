import pathlib


def read_txt_file(file_path: str | pathlib.Path) -> set[str]:
    with open(file_path, encoding='utf-8') as file:
        return set(file.read().strip().split('\n'))
