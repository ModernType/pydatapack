from typing import List
from structures.item import Item
from structures.entity import Selector
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

#! Importing complex commands from their modules

from .scoreboard import *
from .execute import *
from .bossbar import *
from .xp import *

