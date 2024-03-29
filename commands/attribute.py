from __future__ import annotations
from .decorators import command
from typing import Literal
from structures.entity import Selector
from structures.enums import AttributeName

__all__ = ["attribute"]


class attribute_modifier:
    def __init__(self, attr: attribute) -> None:
        self.attr = attr
    
    @command
    def add(self, uuid: str, name: str, value: float, operation: Literal["add", "multiply", "multiply_base"]):
        return f"attribute {self.attr.target} {self.attr.name} modifier add {uuid} {name} {value} {operation}"
    
    @command
    def remove(self, uuid: str):
        return f"attribute {self.attr.target} {self.attr.name} modifier remove {uuid}"
    
    @command
    def value_get(self, uuid: str, scale: float = 1):
        return f"attribute {self.attr.target} {self.attr.name} modifier value get {uuid} {scale}"


class attribute_base:
    def __init__(self, attr: attribute) -> None:
        self.attr = attr

    @command
    def get(self, scale: float = None):
        if scale is None:
            return f"attribute {self.attr.target} {self.attr.name} base get"
        return f"attribute {self.attr.target} {self.attr.name} base get {scale}"
    
    @command
    def set(self, value: float):
        return f"attribute {self.attr.target} {self.attr.name} base set {value}"


class attribute:
    """
    Minecraft `attribute` command. Needs initialization. Subcommands:
    
    - `attribute().get()`
    - `attribute().base()` (has subcommands)
    - `attribute().modifier()` (has subcommands)
    
    ### Example
    
    ```python
    attribute(Selector(), AttributeName.max_health).base().set(30.0)
    ```
    """
    def __init__(self, target: Selector, attribute: AttributeName | str) -> None:
        self.target = target
        self.name = attribute.without_quotes()
    
    @command
    def get(self, scale: float = None):
        if scale is None:
            return f"attribute {self.target} {self.name} get"
        return f"attribute {self.target} {self.name} get {scale}"
    
    def base(self) -> attribute_base:
        return attribute_base(self)
    
    def modifier(self) -> attribute_modifier:
        return attribute_modifier(self)
