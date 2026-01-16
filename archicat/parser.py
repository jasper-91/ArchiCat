from .transformer import ScratchFileBuilder

from lark import Lark,Tree
from pathlib import Path


with open(Path(__file__).parent / 'grammar.lark') as file:
    parser = Lark(file.read())

def parse(text: str) -> Tree:
    return parser.parse(text)

def parse_file(path: Path | str) -> Tree:
    with open(str(path)) as file:
        return parse(file.read())