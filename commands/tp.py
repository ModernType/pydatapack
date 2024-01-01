from typing import overload, Tuple, Literal
from structures import Coords, Selector
from .decorators import command, _cancel_last

__all__ = ["tp", "teleport"]


class tp:
    @overload
    def __init__(self, targets: Selector, destination: Selector): ...
    @overload
    def __init__(self, targets: Selector, location: Coords): ...
    @overload
    def __init__(self, targets: Selector, location: Coords, rotation: Tuple[float, float]): ...
    
    def __init__(self, targets: Selector, destination: Selector | Coords, rotation: Tuple[float, float] = None) -> None:
        @command
        def do():
            self.out = f"tp {targets} {destination if isinstance(destination, Selector) else destination}"
            if rotation is not None:
                self.has_rotation = True
                self.out += f" {rotation}"
            return self.out
        
        do()

    @command
    def facing(self, location: Coords):
        if hasattr(self, "has_rotation"):
            raise RuntimeError("This tp function already defined rotation during main command")
        _cancel_last()
        self.out += f" facing {location}"
        return self.out
    
    @command
    def facing_entity(self, target: Selector, anchor: Literal["eyes", "foot"] = None):
        _cancel_last()
        self.out += f" facing entity {target}"
        if anchor is not None:
            self.out += f" {anchor}"
        return self.out


teleport = tp
