from .transformer import ScratchFileBuilder
from .parser import parse

from pathlib import Path


def transpile(source: str,target: Path | str):
    target = str(target)
    builder = ScratchFileBuilder()
    builder.visit(parse(source))
    builder.save(target)

def transpile_file(source: Path | str,target: Path | str):
    with open(str(source)) as file:
        transpile(file.read(),target)

