from typing import List, Literal
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
    def __init__(self,
                 *,
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
                 tags: List[str] = None,
                 team: str = None,
                 motion: List[float, float, float] = None,
                 rotation: List[float, float] = None,
                 hand_items: List[Item, Item] = None,
                 armor_items: List[Item, Item, Item, Item] = None,
                 hand_drop_chances: List[float, float] = None,
                 armor_drop_chances: List[float, float, float, float] = None,
                 active_effects: List[Effect],
                 attributes: List[AttributeModifier]
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


SORT_LITERAL = Literal["nearest", "furtherst", "random", "arbitrary"]
class Selector:
    def __init__(self,
                 selector: SelectorEnum | str = SelectorEnum.executor,
                 type: EntityId = None,
                 nbt: EntityNBT = None,
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
                 team: str = None,
                 name: str = None,
                 predicate: str = None, # TODO: Maybe there will be some class in future
                 level: int = None,
                 gamemode: GamemodeName = None,
                 limit: int = None,
                 sort: SORT_LITERAL = None
                 ) -> None:
        self.selector = selector
        self.type = type
        self.nbt = nbt
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


class Entity:
    def __init__(self,
                 selector: Selector | EntityId | str = Selector.executor,
                 coordinates: List[Coord, Coord, Coord] = None,
                 nbt: EntityNBT = EntityNBT()
                 ) -> None:
        self.selector = selector
        self.coordinates = coordinates
        self.nbt = nbt

