from __future__ import annotations
from typing import Literal, Tuple
from .decorators import command_macro, _cancel_last
from structures.entity import Selector
from structures.general import Coord


class execute_if:
    def __init__(self, ex: execute):
        self.ex = ex


class execute_positioned:
    def __init__(self, ex) -> None:
        self.ex = ex


class execute:
    def __init__(self) -> None:
        self.command = "execute "

    def align(self, axis: str) -> execute:
        self.command += f"align {axis} "
        return self
    
    anchor = Literal["eyes", "feet"]
    def anchored(self, anchor: anchor):
        self.command += f"anchored {anchor} "
        return self
    
    def as_(self, selector: Selector):
        self.command += f"as {selector} "
        return self
    
    def at(self, selector: Selector):
        self.command += f"at {selector}"
        return self
    
    def facing(self, target: Tuple[Coord, Coord, Coord] | Selector):
        if isinstance(target, Tuple[Coord, Coord, Coord]):
            self.command += f"facing {" ".join(map(str, target))}"
        elif isinstance(target, Selector):
            self.command += f"facing entity {target}"
        else:
            raise TypeError("You should pass Tuple[Coord, Coord, Coord] or Selector type")
        
        return self
    
    def if_(self):
        return execute_if(self)
    
    dimensions = Literal["minecraft:overworld", "minecraft:the_end", "minecraft:the_nether"]
    def in_(self, dimension: dimensions | str):
        self.command += f"in {dimension}"
        return self
    
    on_vars = Literal["attacker", "controller", "leasher", "origin", "owner", "passengers", "target", "vehicle"]
    def on(self, arg: on_vars):
        self.command += f"on {arg}"
        return self
    
    def positioned(self):
        return execute_positioned(self)


    @command_macro
    def run(self, command):
        """Chain of execute commands should end with this method. `command` parameter should be called `@command_macro` decorated function.
        
        ### Example:
        ```
        execute().as_(Selector("@a")).run(say("Something"))
        ```
        will be interpreted in minecraft as:
        ```
        execute as @a run say Something
        ```
        """
        self.command += f"run {command}"
        _cancel_last()
        return self.command
