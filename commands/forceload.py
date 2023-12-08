from .decorators import command_static
from structures.general import Coords

__all__ = ["forceload"]


class forceload:
    @command_static
    def add(from_: Coords, to: Coords | None = None):
        out = f"forceload add {" ".join(map(str, from_))}"
        if to is not None:
            out += f" {" ".join(map(str, to))}"
        return out
    
    @command_static
    def remove(from_: Coords, to: Coords | None = None):
        out = f"forceload remove {" ".join(map(str, from_))}"
        if to is not None:
            out += f" {" ".join(map(str, to))}"
        return out
    
    @command_static
    def query(pos: Coords | None):
        if pos:
            return f"forceload query {" ".join(map(str, pos))}"
        return "forceload query"
