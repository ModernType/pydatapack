from .general import TagClass
from .item import Item

class Inventory(TagClass):
    do_camel_case = False
    
    def __init__(self,
                 mainhand: Item,
                 offhand: Item,
                 head: Item,
                 chest: Item,
                 legs: Item,
                 boots: Item
                 ) -> None:
        self.mainhand = mainhand
        self.offhand = offhand
        self.head = head
        self.chest = chest
        self.legs = legs
        self.boots = boots
    

class EntityNBT:
    def __init__(self) -> None:
        pass


class Entity:
    def __init__(self,
                 selector: str = "@s"
                 ) -> None:
        pass

