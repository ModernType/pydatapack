from structures.entity import Selector
from .decorators import command, command_static
from typing import Literal

__all__ = ("xp", "experience")


class xp:
    """
    Minecraft `xp` command. Subcommands:
    - `xp.add()`
    - `xp.set()`
    - `xp.query()`
    """
    
    @command_static
    def add(target: Selector, amount: int, type_: Literal["levels", "points"]):
        return f"xp add {target} {amount} {type_}"
    
    @command_static
    def set(target: Selector, amount: int, type_: Literal["levels", "points"]):
        return f"xp set {target} {amount} {type_}"
    
    @command_static
    def query(target: Selector, type_: Literal["levels", "points"]):
        return f"xp query {target} {type_}"

experience = xp