from .decorators import command_static
from structures.general import Coords

__all__ = ["forceload"]


class forceload:
    """
    Minecraft `forceload` command. Subcommands:
    - `forceload.add()`
    - `forceload.remove()`
    - `forceload.query()`
    """
    
    @command_static
    def add(from_: Coords, to: Coords | None = None):
        out = f"forceload add {from_}"
        if to is not None:
            out += f" {to}"
        return out
    
    @command_static
    def remove(from_: Coords, to: Coords | None = None):
        out = f"forceload remove {from_}"
        if to is not None:
            out += f" {to}"
        return out
    
    @command_static
    def query(pos: Coords | None):
        if pos:
            return f"forceload query {pos}"
        return "forceload query"
