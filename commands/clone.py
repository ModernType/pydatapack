from structures.general import Coords
from .decorators import command_macro
from typing import Literal

__all__ = ["clone"]


class clone:
    def __init__(self, begin: Coords, end: Coords, destination: Coords) -> None:
        self.begin = begin
        self.end = end
        self.destination = destination
        self._from = None
        self._to = None
    
    dimensions = Literal["minecraft:overworld", "minecraft:the_end", "minecraft:the_nether"]
    def from_(self, dimension: dimensions):
        self._from = dimension
        return self
    
    def to(self, dimension: dimensions):
        self._to = dimension
        return self
    
    def _gen_begining(self):
        out = "clone "
        if self._from is not None:
            out += f"from {self._from}"
        out += f"{" ".join(map(str, self.begin))} {" ".join(map(str, self.end))} "
        if self._to is not None:
            out += f"to {self._to} "
        out += f"{" ".join(map(str, self.destination))} "
        return out

    mode = Literal["force", "move", "normal"]
    @command_macro
    def replace(self, mode: mode = "normal"):
        return f"{self._gen_begining()} replace {mode}"
    
    @command_macro
    def masked(self, mode: mode = "normal"):
        return f"{self._gen_begining()} masked {mode}"
    
    @command_macro
    def filtered(self, filter: str, mode: mode = "normal"): #TODO: filter will be BlockId
        return f"{self._gen_begining()} filtered {filter} {mode}"
