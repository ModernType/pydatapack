from typing import List
from structures.item import Item
from .decorators import command_macro, mc_function

#! Simple commands implementations

@command_macro
def give(item: Item, player: str = "@s"):
    return f"give {player} {item.give_string()}"


@command_macro
def say(text: str):
    return f"say {text}"

#! Importing complex commands from their modules

from .scoreboard import *
from .bossbar import *

