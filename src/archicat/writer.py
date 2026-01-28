from pydantic.dataclasses import dataclass
from dataclasses import field
from typing import Any,Optional


class Writer:
    def generate_code(self) -> str: pass

class Chain[T = Writer](list[T]):
    def generate_code(self) -> str:
        return '{' + '\n'.join(self) + '}'
    
class Declaration(Writer): pass
    
class Value(Writer):
    value: str

    def __init__(self,value: str | int | float | bool):
        if isinstance(value,bool):
            self.value = 'true' if self.value else 'false'
        else:
            self.value = repr(value)

    def generate_code(self):
        return self.value
    
class Path(Writer):
    path: str

    def generate_code(self):
        return '"' + self.path + '"'

@dataclass
class ListValue(Writer):
    values: list[Value] = field(default_factory=list)

    def generate_code(self):
        return f'[{','.join(map(to_code,self.values))}]'
    
@dataclass
class Identifier(Writer):
    name: str

    def generate_code(self):
        return self.name    
    
@dataclass
class Option(Identifier):
    def generate_code(self):
        return '$' + super().generate_code()
    
class Options(Writer):
    options: dict[str,Value]

    def __init__(self,**options):
        self.options = options

    def generate_code(self):
        return '{' + '\n'.join([f'{name} = {value}' for name,value in self.options.items()]) + '}'
    
@dataclass
class BlockCall(Writer):
    name: str
    args: tuple[Value | 'BlockCall' | Chain | Identifier,...] = ()

    def generate_code(self):
        return f'{self.name}({','.join(map(to_code,self.args))})'
    
@dataclass
class Comment(Declaration):
    content: str
    options: Options
    
    def generate_code(self):
        return f': "{self.content}" {to_code(self.options)}'
    
@dataclass
class VariableDeclaration(Declaration):
    name: str
    value: Optional[Value] = None

    def generate_code(self):
        if self.value is None:
            return f'var {self.name}'
        else:
            return f'var {self.name} = {to_code(self.value)}'
        
@dataclass
class ListDeclaration(Declaration):
    name: str
    value: ListValue = field(default_factory=ListValue)

    def generate_code(self):
        return f'list {self.name} = {to_code(self.value)}'
    
@dataclass
class MessageDeclaration(Declaration):
    name: str

    def generate_code(self):
        return f'message {self.name}'
    
@dataclass
class CostumeDeclaration(Declaration):
    name: str
    path: Path

    def generate_code(self):
        return f'costume {self.name} = {to_code(self.path)}'
    
@dataclass
class SoundDeclaration(Declaration):
    name: str
    path: Path

    def generate_code(self):
        return f'sound {self.name} = {to_code(self.path)}'
    
@dataclass
class ProcedureDeclaration(Declaration):
    name: str
    args: tuple[str,...] = ()
    position: Optional[tuple[int,int]] = None
    warp: bool = False

    def generate_code(self):
        if self.warp:
            return f'warp {self.name}({','.join(self.args)})' \
                + ('' if self.position is None else f'[{self.position[0]},{self.position[1]}]')
        else:
            return f'proc {self.name}({','.join(self.args)})' \
                + ('' if self.position is None else f'[{self.position[0]},{self.position[1]}]')
        
@dataclass
class Event(Declaration):
    block: BlockCall
    chain: Chain
    position: Optional[tuple[int,int]] = None

    def generate_code(self):
        return f'on {to_code(self.block)} {to_code(self.chain)}' \
            + ('' if self.position is None else f'[{self.position[0]},{self.position[1]}]')
    
@dataclass
class Configuration(Declaration):
    def generate_code(self):
        return f'config {super().generate_code()}'
    
@dataclass
class Target(Writer):
    name: str
    declarations: Chain[Declaration] = field(default_factory=Chain[Declaration])

    def generate_code(self):
        return f'sprite {self.name} {to_code(self.declarations)}'   



def to_code(writer: Writer) -> str:
    return writer.generate_code()