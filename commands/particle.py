from typing import Literal, overload, Tuple
from .decorators import command
from structures import BlockId, Item, Coords, Selector

__all__ = ["Particle", "particle"]

particles = Literal[
    "ambient_entity_effect",
    "angry_villager",
    "ash",
    "block",
    "block_marker",
    "bubble",
    "bubble_column_up",
    "bubble_pop",
    "campfire_cosy_smoke",
    "cherry_leaves",
    "cloud",
    "composter",
    "crimson_spore",
    "crit",
    "current_down",
    "damage_indicator",
    "dolphin",
    "dragon_breath",
    "dripping_dripstone_lava",
    "dripping_dripstone_water",
    "dripping_honey",
    "dripping_lava",
    "dripping_obsidian_tear",
    "dripping_water",
    "dust",
    "dust_color_transition",
    "dust_plume",
    "effect",
    "egg_crack",
    "elder_guardian",
    "electric_spark",
    "enchant",
    "enchanted_hit",
    "end_rod",
    "entity_effect",
    "explosion",
    "explosion_emitter",
    "falling_dripstone_lava",
    "falling_dripstone_water",
    "falling_dust",
    "falling_honey",
    "falling_lava",
    "falling_nectar",
    "falling_obsidian_tear",
    "falling_spore_blossom",
    "falling_water",
    "firework",
    "fishing",
    "flame",
    "flash",
    "glow",
    "glow_squid_ink",
    "gust",
    "happy_villager",
    "heart",
    "instant_effect",
    "item",
    "item_slime",
    "item_snowball",
    "landing_honey",
    "landing_lava",
    "landing_obsidian_tear",
    "large_smoke",
    "lava",
    "mycelium",
    "nautilus",
    "note",
    "poof",
    "portal",
    "rain",
    "reverse_portal",
    "scrape",
    "sculk_charge_pop",
    "sculk_soul",
    "shriek",
    "small_flame",
    "smoke",
    "sneeze",
    "snowflake",
    "sonic_boom",
    "soul",
    "soul_fire_flame",
    "spit",
    "splash",
    "spore_blossom_air",
    "squid_ink",
    "sweep_attack",
    "totem_of_undying",
    "underwater",
    "vibration",
    "warped_spore",
    "wax_off",
    "wax_on",
    "white_ash",
    "witch"
]


class Particle:
    @overload
    def __init__(self, particle: particles): ...
    @overload
    def __init__(self, particle: Literal["block", "block_marker", "falling_dust"], block: BlockId, block_state: str): ...
    @overload
    def __init__(self, particle: Literal["dust"], r: float, g: float, b: float, size: float): ...
    @overload
    def __init__(self, particle: Literal["dust_color_transition"], start_color: Tuple[float, float, float], end_color: Tuple[float, float, float], size: float): ...
    @overload
    def __init__(self, particle: Literal["item"], item: Item): ...
    @overload
    def __init__(self, particle: Literal["sculk_charge"], angle: float): ...
    @overload
    def __init__(self, particle: Literal["shriek"], delay: int): ...
    @overload
    def __init__(self, particle: Literal["vibration"], pos_to: Tuple[float, float, float], duration: int): ...

    def __init__(self, particle: particles, *args) -> None:
        special = {"block", "block_marker", "falling_dust", "dust", "dust_color_transition", "item", "sculk_charge", "shriek", "vibration"}
        if particle in special and not args:
            raise RuntimeError("You should provide extra parameters for this particle")
        if particle == "item":
            self.output = f"minecraft:{particle} {args[0].give_string()[:-2]}"
        else:
            self.output = f"minecraft:{particle} {" ".join(map(str, args))}"
    
    def __str__(self) -> str:
        return self.output
    
    def __repr__(self) -> str:
        return self.output


@command
def particle(particle: Particle, pos: Coords, delta: Coords, speed: float, count: int, mode: Literal["force", "normal"] = None, viewers: Selector = None):
    out = f"particle {particle} {pos} {delta} {speed} {count}"
    if mode:
        out += f" {mode}"
    if viewers:
        out += f" {viewers}"
    return out
