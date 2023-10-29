from .decorators import command_macro
from structures.entity import Selector
from structures.general import Coords
from typing import Literal, overload

__all__ = ["damage"]


class damage:
    damage_types = Literal["minecraft:arrow",
                           "minecraft:bad_respawn_point",
                           "minecraft:cactus",
                           "minecraft:cramming",
                           "minecraft:dragon_breath",
                           "minecraft:drown",
                           "minecraft:dry_out",
                           "minecraft:explosion",
                           "minecraft:fall",
                           "minecraft:falling_anvil",
                           "minecraft:falling_block",
                           "minecraft:falling_stalactite",
                           "minecraft:fireball",
                           "minecraft:fireworks",
                           "minecraft:fly_into_wall",
                           "minecraft:freeze",
                           "minecraft:generic",
                           "minecraft:generic_kill",
                           "minecraft:hot_floor",
                           "minecraft:in_fire",
                           "minecraft:in_wall",
                           "minecraft:indirect_magic",
                           "minecraft:lava",
                           "minecraft:lightning_bolt",
                           "minecraft:magic",
                           "minecraft:mob_attack",
                           "minecraft:mob_attack_no_aggro",
                           "minecraft:mob_projectile",
                           "minecraft:on_fire",
                           "minecraft:out_of_world",
                           "minecraft:outside_border",
                           "minecraft:player_attack",
                           "minecraft:player_explosion",
                           "minecraft:sonic_boom",
                           "minecraft:stalagmite",
                           "minecraft:starve",
                           "minecraft:sting",
                           "minecraft:sweet_berry_bush",
                           "minecraft:thorns",
                           "minecraft:thrown",
                           "minecraft:trident",
                           "minecraft:unattributed_fireball",
                           "minecraft:wither",
                           "minecraft:wither_skull"
                           ]

    @command_macro
    def __init__(self, target: Selector, amount: int, damage_type: damage_types = None) -> None:
        if damage_type is None:
            return f"damage {target} {amount}"
        return f"damage {target} {amount} {damage_type}"
    
    @staticmethod
    @command_macro
    def at(target: Selector, amount: int, damage_type: str, location: Coords):
        return f"damage {target} {amount} {damage_type} at {" ".join(map(str, location))}"
    
    @overload
    def by(target: Selector, amount: int, damage_type: str, by: Selector): ...
    @overload
    def by(target: Selector, amount: int, damage_type: str, by: Selector, from_: Selector): ...
    @staticmethod
    @command_macro
    def by(target: Selector, amount: int, damage_type: str, by: Selector, from_: Selector = None):
        if from_ is None:
            return f"damage {target} {amount} {damage_type} by {by}"
        return f"damage {target} {amount} {damage_type} by {by} from {from_}"
