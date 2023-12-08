from structures.entity import Selector
from .decorators import command
from typing import Literal

__all__ = ("xp", "experience")


class xp:
    @staticmethod
    @command
    def add(target: Selector, amount: int, type_: Literal["levels", "points"]):
        return f"xp add {target} {amount} {type_}"
    
    @staticmethod
    @command
    def set(target: Selector, amount: int, type_: Literal["levels", "points"]):
        return f"xp set {target} {amount} {type_}"
    
    @staticmethod
    @command
    def query(target: Selector, type_: Literal["levels", "points"]):
        return f"xp query {target} {type_}"

experience = xp