from typing import List, Literal, overload, Tuple
from structures.item import Item
from structures.entity import Selector
from structures.enums import GamemodeName, EnchantmentId, minecraft_biomes, BlockId
from structures.general import Coords, Coord
from structures.text import Text
from structures.entity import EntityId, EntityNBT
# from .decorators import _cancel_last
from .decorators import *
from core import MCFunc

#! Simple commands implementations

@command
def give(item: Item, player: str = "@s"):
    """Standard minecraft give command"""
    return f"give {player} {item.give_string()}"

@command
def say(text: str):
    """Standard minecraft say command"""
    return f"say {text}"

@command
def clear(selector: Selector, item: Item, max_count: int = 1):
    """Standard minecraft clear command"""
    return f"clear {selector} {item.give_string()[:-2]} {max_count}"

@command
def kill(target: Selector):
    """Standard minecraft kill command"""
    return f"kill {target}"

@command
def difficulty(difficulty: Literal["peaceful", "easy", "normal", "hard"]):
    """Standard minecraft difficulty command"""
    return f"difficulty {difficulty}"

@command
def gamemode(mode: GamemodeName | str, target: Selector = None):
    """Standard minecraft gamemode command"""
    if target is None:
        target = Selector()
    return f"gamemode {mode} {target}"

@command
def enchant(targets: Selector, enchantment: EnchantmentId, level: int | None = None):
    """Standard minecraft enchant command"""
    out = f"enchant {targets} {enchantment}"
    if level is not None:
        out += f" {level}"
    return out

@command
def fillbiome(from_: Coords, to: Coords, biome: minecraft_biomes | str, replace: minecraft_biomes | str | None = None):
    """Standard minecraft fillbiome command"""
    out = f"fillbiome {from_} {to} {biome}"
    if replace is not None:
        out += f" replace {replace}"
    return out

@command
def tellraw(targets: Selector, message: Text):
    return f"tellraw {targets} {"[\"\", " + str(message)[1:]}"

@command
def weather(weather: Literal["clear", "rain", "thunder"], duration: int = None):
    out = f"weather {weather}"
    if duration is not None:
        out += f" {duration}"
    return out

@overload
def return_(value: int): ...
@overload
def return_(run: MCFunc): ...

@command
def return_(val):
    if isinstance(val, int):
        return f"return {val}"
    elif isinstance(val, MCFunc):
        return f"return run {val}"
    else:
     raise RuntimeError("Wrong return value. Should be int or command result")

@command
def summon(entity: EntityId, pos: Coords = None, nbt: EntityNBT = None):
    out = f"summon {entity}"
    if pos:
        out += f" {pos}"
    if nbt:
        out += f" {nbt}"
    return out

@command
def setblock(pos: Coords, block: BlockId, mode: Literal["destroy", "keep", "replace"] = None):
    out = f"setblock {pos} {block}"
    if mode:
        out += f" {mode}"
    return mode

@command
def spawnpoint(targets: Selector, pos: Coords = None, angle: float = None):
    out = f"spawnpoint {targets}"
    if pos:
        out += f" {pos}"
    if angle:
        out += f" {angle}"
    return out


@overload
def spectate(): ...
@overload
def spectate(target: Selector, player: Selector = None): ...

@command
def spectate(target: Selector = None, player: Selector = None):
    if target is None:
        return "spectate"
    
    out = f"spectate {target}"
    if player:
        out += f" {player}"
    
    return out

@command
def spreadplayers(center: Tuple[Coord, Coord], spread_dist: float, max_range: float, respect_teams: bool, targets: Selector):
    return f"spreadplayers {" ".join(center)} {spread_dist} {max_range} {str(respect_teams).lower()} {targets}"

@command
def spreadplayers_under(center: Tuple[Coord, Coord], spread_dist: float, max_range: float, max_height: float, respect_teams: bool, targets: Selector):
    return f"spreadplayers {" ".join(center)} {spread_dist} {max_range} under {max_height} {str(respect_teams).lower()} {targets}"

@command
def fill(from_: Coords, to: Coords, block: BlockId, mode: Literal["destroy", "hollow", "keep", "outline", "replace"] = None):
    out = f"fill {from_} {to} {block}"
    if mode:
        out += f" {mode}"
    return out

#! Commands based on class

class time:
    @command_static
    def add(amount: int):
        return f"time add {amount}"
    
    @command_static
    def query(mode: Literal["daytime", "gametime", "day"]):
        return f"time query {mode}"
    
    @command_static
    def set(time: Literal["day", "night", "noon", "midnight"] | int):
        return f"time set {time}"


class schedule:
    @command_static
    def function(function: MCFunc, time: int, mode: Literal["append", "replace"] = None):
        out = f"schedule function {function} {time}"
        if mode:
            out += f" {mode}"
        return out
    
    @command_static
    def clear(function: MCFunc):
        return f"schedule clear {function}"


class title:
    def __init__(self, targets: Selector):
        self.targets = targets
    
    @command
    def clear(self):
        return f"title {self.targets} clear"
    
    @command
    def reset(self):
        return f"title {self.targets} reset"
    
    @command
    def title(self, text: Text):
        return f"title {self.targets} title {text}"
    
    @command
    def subtitle(self, text: Text):
        return f"title {self.targets} subtitle {text}"
    
    @command
    def actionbar(self, text: Text):
        return f"title {self.targets} actionbar {text}"
    
    @command
    def times(self, fade_in: int, stay: int, fade_out: int):
        return f"title {self.targets} times {fade_in} {stay} {fade_out}"
    

class ride:
    @command_static
    def mount(targets: Selector, vehicle: Selector):
        return f"ride {targets} mount {vehicle}"
    
    @command_static
    def dismount(targets: Selector):
        return f"ride {targets} dismount"


class random:
    @command_static
    def value(range: str, sequence: str = None): # TODO: replace range
        out = f"random value {range}"
        if sequence:
            out += f" {sequence}"
        return out
    
    @command_static
    def roll(range: str, sequence: str = None): # TODO: replace range
        out = f"random roll {range}"
        if sequence:
            out += f" {sequence}"
        return out

    @command_static
    def reset(sequence: Literal["*"] | str, seed: int = None, include_world_seed: bool = None, include_sequence_id: bool = None):
        out = f"random reset {sequence}"
        if seed:
            out += f" {seed}"
        if include_world_seed:
            out += f" {str(include_world_seed).lower()}"
        if include_sequence_id:
            out += f" {str(include_sequence_id).lower()}"
        return out
        


#! Importing complex commands from their modules

from .scoreboard import *
from .execute import *
from .bossbar import *
from .xp import *
from .attribute import *
from .clone import *
from .damage import *
from .effect import *
from .forceload import *
from .tag import *
from .tp import *
from .trigger import *
from .item import *
from .sound import *
from .particle import *
from .team import *
from .data import *
