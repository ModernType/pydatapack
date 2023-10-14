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
        self.name = name
        self.lore = lore


class Item(TagClass):
    def __init__(self,
                 id: ItemId | str,
                 unbreakable: bool = False,
                 attribute_modifiers: List[AttributeModifier] = None,
                 custom_model_data: int | None = None,
                 display: dict = None,
                 enchantments: List[Enchantment] = None,
                 count: int = 1,
                 damage: int = 0,
                 can_destroy: List[ItemId | str] = None,
                 can_place_on: List[ItemId | str] = None,
                 hide_flags: int | None = None,
                 repair_cost: int = 0,
                 **kwargs
                 ) -> None:
        self.id = id
        self.unbreakable = unbreakable
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
        self.custom_props = kwargs
    
    def give_string(self): # variant special for 'give' command
        base = self.id.without_quotes() + "{" if isinstance(self.id, ItemId) else self.id + "{"
        additions = []
        if self.unbreakable:
            additions.append(f"Unbreakable:{int(self.unbreakable)}b")
        if self.attribute_modifiers is not None:
            additions.append(f"AttributeModifiers:{self.attribute_modifiers}")
        if self.can_destroy is not None:
            additions.append(f"CanDestroy:{self.can_destroy}")
        if self.can_place_on is not None:
            additions.append(f"CanPlaceOn:{self.can_place_on}")
        if self.custom_model_data is not None:
            additions.append(f"CustomModelData:{self.custom_model_data}")
        if self.damage:
            additions.append(f"Damage:{self.damage}")
        if self.display is not None:
            additions.append(f"display:{self.display}")
        if self.enchantments is not None:
            additions.append(f"Enchantments:{self.enchantments}")
        if self.hide_flags is not None:
            additions.append(f"HideFlags:{self.hide_flags}")
        if self.repair_cost:
            additions.append(f"RepairCost:{self.repair_cost}")

        for k, v in self.custom_props.items():
            additions.append(f"{k}:{v}")

        if additions:
            base += ",".join(additions)
        return base + "} " + str(self.count)

    def __str__(self) -> str: # We modify this method because some properties don't start with capital letter
        return super().__str__().replace("Id", "id", 1).replace("Display", "display", 1)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __setitem__(self, key, val):
        return self.__setattr__(key, val)
    
        