from __future__ import annotations
from typing import Literal, overload
from .decorators import command_macro, _cancel_last
from .scoreboard import ScoreBoard
from structures.entity import Selector
from structures.general import Coords
from structures.enums import EntityId

__all__ = ["execute"]


class execute_if_data:
    def __init__(self, ex: execute, prefix: str):
        self.ex = ex
        self.prefix = prefix

    def block(self, pos: Coords, path: str) -> execute:
        self.ex._append(f"{self.prefix} data block {" ".join(map(str, pos))} {path}")
        return self.ex

    def entity(self, target: Selector, path: str) -> execute:
        self.ex._append(f"{self.prefix} data block {target} {path}")
        return self.ex

    def storage(self, source: str, path: str) -> execute:
        self.ex._append(f"{self.prefix} data block {source} {path}")
        return self.ex

class execute_if:
    def __init__(self, ex: execute, unless: bool = False):
        self.ex = ex
        if unless:
            self.prefix = "unless"
        else:
            self.prefix = "if"

    def biome(self, pos: Coords, biome: str) -> execute: #TODO: biome enum
        pos = " ".join(map(str, pos))
        self.ex._append(f"{self.prefix} biome {pos} {biome} ")
        return self.ex
    
    def block(self, pos: Coords, block: str) -> execute: #TODO: blocks enum
        pos = " ".join(map(str, pos))
        self.ex._append(f"{self.prefix} block {pos} {block} ")
        return self.ex

    def blocks(self, start: Coords, end: Coords, destination: Coords, mode: Literal["all", "masked"] = "masked") -> execute:
        self.ex._append(f"{self.prefix} blocks {" ".join(map(str, start))} {" ".join(map(str, end))} {" ".join(map(str, destination))} {mode}")
        return self.ex

    def data(self) -> execute_if_data:
        return execute_if_data(self.ex, self.prefix)

    dimensions = Literal["minecraft:overworld", "minecraft:the_end", "minecraft:the_nether"]
    def dimension(self, dimension: dimensions) -> execute:
        self.ex._append(f"{self.prefix} dimension {dimension} ")
        return self.ex
    
    def entity(self, selector: Selector) -> execute:
        self.ex._append(f"{self.prefix} entity {selector} ")
        return self.ex
    
    def loaded(self, pos: Coords) -> execute:
        pos = " ".join(map(str, pos))
        self.ex._append(f"{self.prefix} loaded {pos} ")
        return self.ex
    
    def predicate(self, predicate: str) -> execute: #TODO: There might be predicate object in the future
        self.ex._append(f"{self.prefix} predicate {predicate} ")
        return self.ex

    operations = Literal["<", "=", ">", ">=", "<="]
    @overload
    def score(self, selector: Selector, objective: ScoreBoard | str, operation: operations, compare_selector: Selector, compare_objective: ScoreBoard | str) -> execute: ...
    @overload
    def score(self, selector: Selector, objective: ScoreBoard | str, operation: Literal["matches"], range: str) -> execute: ...
    def score(self, selector: Selector, objective: ScoreBoard | str, operation: operations, compare_selector_or_range, compare_objective: ScoreBoard | str = None) -> execute:
        if operation == "matches":
            self.ex._append(f"{self.prefix} score {selector} {objective} {operation} {compare_selector_or_range} ")
            return self.ex
        if operation in {"<", "=", ">", ">=", "<="}:
            self.ex._append(f"{self.prefix} score {selector} {objective} {operation} {compare_selector_or_range} {compare_objective} ")
            return self.ex
        else:
            raise ValueError("Wrong operation")


class execute_positioned:
    def __init__(self, ex: execute) -> None:
        self.ex = ex
    
    def as_(self, selector: Selector) -> execute:
        self.ex._append(f"positioned as {selector} ")
        return self.ex
    
    over = Literal["motion_blocking", "motion_blocking_no_leaves", "ocean_floor", "world_surface"]
    def over(self, over: over) -> execute:
        self.ex._append(f"positioned over {over}")
        return self.ex


class execute_store:
    type save_type = Literal["byte", "short", "int", "long", "float", "double"]
    
    def __init__(self, ex: execute, res_or_succes: str):
        self.ex = ex
        self.arg = res_or_succes
    
    def block(self, target_pos: Coords, path: str, type_: save_type, scale: float = 1) -> execute:
        self.ex._append(f"store {self.arg} block {target_pos} {path} {type_} {scale}")
        return self.ex
    
    def bossbar(self, id_: str, target: Literal["max", "value"] = "value") -> execute: #TODO: Add bossbar object here
        self.ex._append(f"store {self.arg} bossbar {id_} {target}")
        return self.ex

    def entity(self, selector: Selector, path: str, type_: save_type, scale: float = 1) -> execute:
        self.ex._append(f"store {self.arg} entity {selector} {path} {type_} {scale}")
        return self.ex
    
    def score(self, targets: Selector, objective: ScoreBoard | str) -> execute:
        self.ex._append(f"store {self.arg} score {targets} {objective}")
        return self.ex
    
    def storage(self, storage: str, path: str, type_: save_type, scale: float = 1) -> execute:
        self.ex._append(f"store {self.arg} storage {storage} {path} {type_} {scale}")
        return self.ex

class execute:
    def __init__(self) -> None:
        self.command = "execute "
    
    def _append(self, s: str):
        self.command += s

    def align(self, axis: str) -> execute:
        self.command += f"align {axis} "
        return self
    
    anchor = Literal["eyes", "feet"]
    def anchored(self, anchor: anchor) -> execute:
        self.command += f"anchored {anchor} "
        return self
    
    def as_(self, selector: Selector) -> execute:
        self.command += f"as {selector} "
        return self
    
    def at(self, selector: Selector) -> execute:
        self.command += f"at {selector} "
        return self
    
    def facing(self, target: Coords | Selector) -> execute:
        if isinstance(target, Coords):
            self.command += f"facing {" ".join(map(str, target))} "
        elif isinstance(target, Selector):
            self.command += f"facing entity {target} "
        else:
            raise TypeError("You should pass Tuple[Coord, Coord, Coord] or Selector type")
        
        return self
    
    def if_(self) -> execute_if:
        return execute_if(self)
    
    dimensions = Literal["minecraft:overworld", "minecraft:the_end", "minecraft:the_nether"]
    def in_(self, dimension: dimensions | str) -> execute:
        self.command += f"in {dimension} "
        return self
    
    on_vars = Literal["attacker", "controller", "leasher", "origin", "owner", "passengers", "target", "vehicle"]
    def on(self, arg: on_vars) -> execute:
        self.command += f"on {arg} "
        return self
    
    @overload
    def positioned(self) -> execute_positioned: ...
    @overload
    def positioned(self, coords: Coords) -> execute: ...
    def positioned(self, coords = None):
        if coords is not None:
            self.command += f"positioned {" ".join(map(str, coords))} "
            return self
        return execute_positioned(self)

    def rotated(self, selector: Selector) -> execute:
        self.command += f"rotated as {selector} "
        return self
    
    def summon(self, entity: EntityId | str) -> execute:
        self.command += f"summon {entity.without_quotes() if isinstance(entity, EntityId) else entity} "
        return self
    
    def unless(self) -> execute_if:
        return execute_if(self, True)
    
    # @overload
    # def store(self, arg: Literal["result", "success"]) -> execute_store: ...
    # @overload
    # def store(self, arg: Literal["result", "success"], property): ...
    def store(self, arg: Literal["result", "success"], property = None):
        """Execute subcommand `store`."""
        return execute_store(self, arg)

    @command_macro
    def run(self, command):
        """Chain of execute commands should end with this method. `command` parameter should be any called `@command_macro` decorated function.
        
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
