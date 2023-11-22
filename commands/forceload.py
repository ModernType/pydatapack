from .decorators import static_command_macro
from structures.general import Coords

__all__ = ["forceload"]


class forceload:
    @static_command_macro
    def add(from_: Coords, to: Coords | None = None):
        out = f"forceload add {" ".join(map(str, from_))}"
        if to is not None:
            out += f" {" ".join(map(str, to))}"
        return out
    
    @static_command_macro
    def remove(from_: Coords, to: Coords | None = None):
        out = f"forceload remove {" ".join(map(str, from_))}"
        if to is not None:
            out += f" {" ".join(map(str, to))}"
        return out
    
    @static_command_macro
    def query(pos: Coords | None):
        if pos:
            return f"forceload query {" ".join(map(str, pos))}"
        return "forceload query"
