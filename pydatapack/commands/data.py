from __future__ import annotations
from .decorators import command, command_static
from typing import Any
from structures import Selector, Coords, Storage

__all__ = ["data"]


type target_type = Selector | Coords | Storage


def _format_target(target: target_type) -> str:
    if isinstance(target, Selector):
        return f"entity {target}"
    elif isinstance(target, Coords):
        return f"block {target}"
    elif isinstance(target, Storage):
        return f"storage {target}"
    else:
        raise TypeError("Target argument should be of type Selector or BlockId or Storage")


class data_modify_finisher:
    def __init__(self, cur_com) -> None:
        self.cur_com = cur_com
    
    @command
    def from_(self, target: target_type, source_path: str = None):
        out = f"{self.cur_com} from {target}"
        if source_path:
            out += f" {source_path}"
        return out
    
    @command
    def string(self, target: target_type, source_path: str = None, start: int = None, end: int = None):
        out = f"{self.cur_com} from {target}"
        if source_path:
            out += f" {source_path}"
        if start is not None:
            out += f" {start}"
        if end is not None:
            out += f" {end}"
        return out
    
    @command
    def value(self, value: Any):
        return f"{self.cur_com} {value}"


class data_modify:
    def __init__(self, target, target_path) -> None:
        self.start = f"data modify {_format_target(target)} {target_path}"
    
    def append(self) -> data_modify_finisher:
        return data_modify_finisher(f"{self.start} append")
    
    def index(self, index: int) -> data_modify_finisher:
        return data_modify_finisher(f"{self.start} index {index}")
    
    def merge(self) -> data_modify_finisher:
        return data_modify_finisher(f"{self.start} merge")
    
    def prepand(self) -> data_modify_finisher:
        return data_modify_finisher(f"{self.start} prepand")
    
    def set(self) -> data_modify_finisher:
        return data_modify_finisher(f"{self.start} set")


class data:
    @command_static
    def get(target: target_type, path: str = None, scale: float = None):
        out = f"data get {_format_target(target)}"
        if path:
            out += f" {path}"
        if scale:
            out += f" {scale}"
        return out
    
    @command_static
    def merge(target: target_type, nbt: str): # TODO: Do something with nbt, maybe some `@overload`s
        return f"data merge {_format_target(target)} {nbt}"
    
    @command_static
    def remove(target: target_type, path: str):
        return f"data remove {_format_target(target)} {path}"
    
    def modify(target: target_type, target_path: str) -> data_modify:
        return data_modify(target, target_path)