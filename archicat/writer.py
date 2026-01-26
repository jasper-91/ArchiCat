
class Chain(list[str]):
    def generate_code(self) -> str:
        return '{' + '\n'.join(self) + '}'
    
    def __add__(self,other: str) -> str:
        return self.generate_code() + other
    
    def __radd__(self,other: str) -> str:
        return other + self.generate_code()
