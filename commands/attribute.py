from __future__ import annotations
from .decorators import command_macro
from typing import Literal
from structures.entity import Selector
from structures.enums import AttributeName

__all__ = ["attribute"]


class attribute_modifier:
    def __init__(self, attr: attribute) -> None:
        self.attr = attr
    
    @command_macro
    def add(self, uuid: str, name: str, value: float, operation: Literal["add", "multiply", "multiply_base"]):
        return f"attribute {self.attr.target} {self.attr.name} modifier add {uuid} {name} {value} {operation}"
    
    @command_macro
    def remove(self, uuid: str):
        return f"attribute {self.attr.target} {self.attr.name} modifier remove {uuid}"
    
    @command_macro
    def value_get(self, uuid: str, scale: float = 1):
        return f"attribute {self.attr.target} {self.attr.name} modifier value get {uuid} {scale}"


class attribute_base:
    def __init__(self, attr: attribute) -> None:
        self.attr = attr

    @command_macro
    def get(self, scale: float = None):
        if scale is None:
            return f"attribute {self.attr.target} {self.attr.name} base get"
        return f"attribute {self.attr.target} {self.attr.name} base get {scale}"
    
    @command_macro
    def set(self, value: float):
        return f"attribute {self.attr.target} {self.attr.name} base set {value}"


class attribute:
    def __init__(self, target: Selector, attribute: AttributeName | str) -> None:
        self.target = target
        self.name = attribute
    
    @command_macro
    def get(self, scale: float = None):
        if scale is None:
            return f"attribute {self.target} {self.name} get"
        return f"attribute {self.target} {self.name} get {scale}"
    
    def base(self):
        return attribute_base(self)
    
    def modifier(self):
        return attribute_modifier(self)
