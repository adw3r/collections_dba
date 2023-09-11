from typing import Generator

import pathlib

ENCODING = 'latin-1'


def read_txt_file(file_path: str | pathlib.Path) -> set[str]:
    with open(file_path, encoding=ENCODING) as file:
        return set(file.read().strip().split('\n'))


def read_file_in_chunks(file_name: str | pathlib.Path, chunk_size: int) -> Generator:
    with open(file_name, encoding=ENCODING) as file:
        tmp_lines = file.readlines(chunk_size)
        while tmp_lines:
            yield set(tmp_lines)
            tmp_lines = file.readlines(chunk_size)
