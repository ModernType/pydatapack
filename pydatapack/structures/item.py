from __future__ import annotations
from typing import List
from .enums import *
from .text import Text
from .general import TagClass, AttributeModifier


class Enchantment(TagClass):
    do_camel_case = False

    def __init__(self,
                 id: EnchantmentId | str,
                 lvl: int = 0
                 ) -> None:
        self.id = id
        self.lvl = lvl


class Display(TagClass):
    def __init__(self,
                 name: Text | str = None, # Name should be defined only with formating at the start
                 lore: Text | str = None
                 ) -> None:
        if isinstance(name, Text):
            name.quotes = True
        self.name = name
        if isinstance(lore, Text):
            lore.quotes = True
        self.lore = lore


class Item(TagClass):
    exceptions = {"id", "display"}
    
    def __init__(self,
                 id: ItemId | str,
                 unbreakable: bool = None,
                 tags: List[str] = None,
                 attribute_modifiers: List[AttributeModifier] = None,
                 custom_model_data: int | None = None,
                 display: Display = None,
                 enchantments: List[Enchantment] = None,
                 count: int = 1,
                 damage: int = None,
                 can_destroy: List[ItemId | str] = None, # TODO: Change ItemId to BlockId
                 can_place_on: List[ItemId | str] = None, # TODO: Change ItemId to BlockId
                 hide_flags: int | HideFlags = None,
                 repair_cost: int = None,
                 **kwargs
                 ) -> None:
        self.id = id
        self.unbreakable = unbreakable
        self.tags = tags
        self.attribute_modifiers = attribute_modifiers
        self.can_destroy = can_destroy
        self.can_place_on = can_place_on
        self.custom_model_data = custom_model_data
        self.damage = damage
        self.display = display 
        self.enchantments = enchantments 
        self.count = count
        self.hide_flags = hide_flags
        self.repair_cost = repair_cost
        for k, v in kwargs.items():
            self.__setattr__(k, v)
    
    def give_string(self): # variant special for 'give' command
        self.ignore.add("id")
        self.ignore.add("count")
        out = f"{str(self.id).strip('"')}{self.__str__()} {self.count}"
        self.ignore.remove("id")
        self.ignore.remove("count")
        return out

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __setitem__(self, key, val):
        return self.__setattr__(key, val)
    
        