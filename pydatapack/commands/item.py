from .decorators import command, command_static
from structures import Selector, BlockId, Item

__all__ = ["item"]

"""
Slots:
- armor.chest
- armor.feet 		
- armor.head 
- armor.legs 
- weapon 		
- weapon.mainhand
- weapon.offhand 
- container.<slot_number>
- enderchest.<slot_number>
- hotbar.<slot_number>
- inventory.<slot_number>
- horse.saddle
- horse.chest
- horse.armor
- horse.<slot_number>
- villager.<slot_number>
"""

class item_replace:
    def __init__(self, target, slot) -> None:
        if isinstance(target, Selector):
            self.start = f"item replace entity {target} {slot}"
        elif isinstance(target, BlockId):
            self.start = f"item replace block {target} {slot}"
        else:
            raise TypeError()
    
    @command
    def with_(self, item: Item):
        return f"{self.start} with {item.give_string()}"
    
    @command
    def from_(self, source: Selector | BlockId, source_slot: str, modifier: str = None):
        out = f"{self.start} from"
        if isinstance(source, Selector):
            out += f" entity"
        elif isinstance(source, BlockId):
            out += f" block"
        else:
            raise TypeError("You shold pass only Selector or BlockId instance")
        out += f" {source} {source_slot}"
        if modifier:
            out += f" {modifier}"
        
        return out


class item:
    @command_static
    def modify(target: Selector | BlockId, slot: str, modifier: str): # TODO: Do something with slots
        if isinstance(target, Selector):
            return f"item modify entity {target} {slot} {modifier}"
        elif isinstance(target, BlockId):
            return f"item modify block {target} {slot} {modifier}"
        else:
            raise TypeError("You shold pass only Selector or BlockId instance")
    
    @staticmethod
    def replace(target: Selector | BlockId, slot: str) -> item_replace: # TODO: Do something with slots
        return item_replace(target, slot)
    