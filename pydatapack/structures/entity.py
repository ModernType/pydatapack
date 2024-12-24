from typing import Tuple, Literal
from .enums import *
from .general import TagClass, Coord
from .item import Item
from .text import Text
from .effect import Effect
from .general import AttributeModifier

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
    

class EntityNBT(TagClass):
    def __init__(self, *,
                 custom_name: Text = None,
                 health: int = None,
                 can_pick_up_loot: bool = None,
                 glowing: bool = None,
                 has_visual_fire: bool = None,
                 invulnerable: bool = None,
                 left_handed: bool = None,
                 no_AI: bool = None,
                 no_gravity: bool = None,
                 persistent: bool = None,
                 silent: bool = None,
                 tags: Tuple[str] = None,
                 team: str = None,
                 motion: Tuple[float, float, float] | None = None,
                 rotation: Tuple[float, float] | None = None,
                 hand_items: Tuple[Item, Item] | None = None,
                 armor_items: Tuple[Item, Item, Item, Item] | None = None,
                 hand_drop_chances: Tuple[float, float] | None = None,
                 armor_drop_chances: Tuple[float, float, float, float] | None = None,
                 active_effects: Tuple[Effect] | None = None,
                 attributes: Tuple[AttributeModifier] | None = None,
                 **kwargs
                 ) -> None:
        self.custom_name = custom_name
        self.health = health
        self.can_pick_up_loot = can_pick_up_loot
        self.glowing = glowing
        self.has_visual_fire = has_visual_fire
        self.invulnerable = invulnerable
        self.left_handed = left_handed
        self.no_AI = no_AI
        self.no_gravity = no_gravity
        self.persistent = persistent
        self.silent = silent
        self.tags = tags
        self.team = team
        self.motion = motion
        self.rotation = rotation
        self.hand_items = hand_items
        self.armor_items = armor_items
        self.hand_drop_chances = hand_drop_chances
        self.armor_drop_chances = armor_drop_chances
        self.active_effects = active_effects
        self.attributes = attributes
        for k, v in kwargs.items():
            self.__setattr__(k, v)


SORT_LITERAL = Literal["nearest", "furtherst", "random", "arbitrary"]
class Selector:
    def __init__(self,
                 selector: SelectorEnum | str = SelectorEnum.executor,
                 *,
                 type: EntityId = None,
                 nbt: EntityNBT = None,
                 score: list[str] = None, # TODO: add here list of scores or something like that
                 x: float = None,
                 y: float = None,
                 z: float = None,
                 dx: float = None,
                 dy: float = None,
                 dz: float = None,
                 distance: float = None,
                 x_rotation: float = None,
                 y_rotation: float = None,
                 tag: str = None,
                 team: str = None, # TODO: add team type when it will be implemented
                 name: str = None,
                 predicate: str = None, # TODO: Maybe there will be some class in future
                 level: int = None,
                 gamemode: GamemodeName | str = None,
                 limit: int = None,
                 sort: SORT_LITERAL = None
                 ) -> None:
        self.selector = selector
        self.type = type
        self.nbt = nbt
        self.score = score
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.distance = distance
        self.x_rotation = x_rotation
        self.y_rotation = y_rotation
        self.tag = tag
        self.team = team
        self.name = name
        self.predicate = predicate
        self.level = level
        self.gamemode = gamemode
        self.limit = limit
        self.sort = sort
    
    def __str__(self):
        out = []
        for k, v in self.__dict__.items():
            if v is not None:
                out.append(f"{k}={v}")
        out.pop(0)
        if not out:
            return f"{self.selector}"
        return f"{self.selector}[{", ".join(out)}]"

    def __repr__(self):
        return self.__str__()


class Entity[T: Coord | float | str]:
    def __init__(self,
                 selector: Selector | EntityId | str = SelectorEnum.executor,
                 coordinates: Tuple[T, T, T] = None,
                 nbt: EntityNBT = EntityNBT()
                 ) -> None:
        self.selector = selector
        self.coordinates = coordinates
        self.nbt = nbt

