from typing import List, Literal
from structures.item import Item
from structures.entity import Selector
from structures.enums import GamemodeName, EnchantmentId, minecraft_biomes
from structures.general import Coords
from structures.text import Text
from .decorators import *

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
    out = f"fillbiome {" ".join(map(str, from_))} {" ".join(map(str, to))} {biome}"
    if replace is not None:
        out += f" replace {replace}"
    return out

@command
def tellraw(targets: Selector, message: Text):
    return f"tellraw {targets} {"[\"\", " + str(message)[1:]}"



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
