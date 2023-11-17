from typing import List, Literal
from structures.item import Item
from structures.entity import Selector
from structures.enums import GamemodeName, EnchantmentId
from .decorators import *

#! Simple commands implementations

@command_macro
def give(item: Item, player: str = "@s"):
    return f"give {player} {item.give_string()}"

@command_macro
def say(text: str):
    return f"say {text}"

@command_macro
def clear(selector: Selector, item: Item, max_count: int = 1):
    return f"clear {selector} {item.give_string()[:-2]} {max_count}"

@command_macro
def kill(target: Selector):
    return f"kill {target}"

@command_macro
def difficulty(difficulty: Literal["peaceful", "easy", "normal", "hard"]):
    return f"difficulty {difficulty}"

@command_macro
def gamemode(mode: GamemodeName | str, target: Selector = None):
    if target is None:
        target = Selector()
    return f"gamemode {mode} {target}"

@command_macro
def enchant(targets: Selector, enchantment: EnchantmentId, level: int | None = None):
    out = f"enchant {targets} {enchantment}"
    if level is not None:
        out += f" {level}"
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
