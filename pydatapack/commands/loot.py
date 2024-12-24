from typing import Literal
from .decorators import command
from structures import Selector, Coords 

__all__ = ["loot"]


class loot_with_target:
    def __init__(self, start_str: str) -> None:
        self.start_str = start_str
    
    @command
    def fish(self, loot_table: str, pos: Coords, tool: str | Literal["mainhand", "offhand"] = None):
        out = f"{self.start_str} fish {loot_table} {pos}"
        if tool:
            out += f" {tool}"
        return out
    
    @command
    def loot(self, loot_table: str):
        return f"{self.start_str} loot {loot_table}"
    
    @command
    def kill(self, target: Selector):
        return f"{self.start_str} kill {target}"
    
    @command
    def mine(self, pos: Coords, tool: str | Literal["mainhand", "offhand"] = None):
        out = f"{self.start_str} mine {pos}"
        if tool:
            out += f" {tool}"
        return out


class loot:
    @staticmethod
    def give(players: Selector) -> loot_with_target:
        return loot_with_target(f"loot give {players}")
    
    @staticmethod
    def insert(target_pos: Coords) -> loot_with_target:
        return loot_with_target(f"loot insert {target_pos}")
    
    @staticmethod
    def spawn(target_pos: Coords) -> loot_with_target:
        return loot_with_target(f"loot insert {target_pos}")
    
    @staticmethod
    def replace_block(target_pos: Coords, slot: int, count: int = None) -> loot_with_target:
        out = f"loot replace block {target_pos} {slot}b"
        if count is not None:
            out += f" {count}"
        return loot_with_target(out)
    
    @staticmethod
    def replace_entity(entities: Selector, slot: int, count: int = None) -> loot_with_target:
        out = f"loot replace entity {entities} {slot}b"
        if count is not None:
            out += f" {count}"
        return loot_with_target(out)
