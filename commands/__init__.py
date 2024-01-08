from typing import List, Literal, overload, Tuple
from structures import Item, Selector, GamemodeName, EnchantmentId, minecraft_biomes, BlockId, Coords, Coord, Text, EntityId, EntityNBT, EffectId
from .decorators import _cancel_last
from .decorators import *
from core import MCFunc

#! Simple commands implementations

@command
def give(item: Item, player: str = "@s"):
    """Standard minecraft give command"""
    return f"give {player} {item.give_string()}"

@command
def say(text: str):
    """Standard minecraft say command"""
    return f"say {text}"

@command
def clear(selector: Selector, item: Item, max_count: int = 1):
    """Standard minecraft clear command"""
    return f"clear {selector} {item.give_string()[:-2]} {max_count}"

@command
def kill(target: Selector):
    """Standard minecraft kill command"""
    return f"kill {target}"

@command
def difficulty(difficulty: Literal["peaceful", "easy", "normal", "hard"]):
    """Standard minecraft difficulty command"""
    return f"difficulty {difficulty}"

@command
def gamemode(mode: GamemodeName | str, target: Selector = None):
    """Standard minecraft gamemode command"""
    if target is None:
        target = Selector()
    return f"gamemode {mode} {target}"

@command
def enchant(targets: Selector, enchantment: EnchantmentId, level: int | None = None):
    """Standard minecraft enchant command"""
    out = f"enchant {targets} {enchantment}"
    if level is not None:
        out += f" {level}"
    return out

@command
def fillbiome(from_: Coords, to: Coords, biome: minecraft_biomes | str, replace: minecraft_biomes | str | None = None):
    """Standard minecraft fillbiome command"""
    out = f"fillbiome {from_} {to} {biome}"
    if replace is not None:
        out += f" replace {replace}"
    return out

@command
def tellraw(targets: Selector, message: Text):
    return f"tellraw {targets} {"[\"\", " + str(message)[1:]}"

@command
def weather(weather: Literal["clear", "rain", "thunder"], duration: int = None):
    out = f"weather {weather}"
    if duration is not None:
        out += f" {duration}"
    return out

@overload
def return_(value: int): ...
@overload
def return_(run: MCFunc): ...

@command
def return_(val):
    if isinstance(val, int):
        return f"return {val}"
    elif isinstance(val, MCFunc):
        return f"return run {val}"
    else:
     raise RuntimeError("Wrong return value. Should be int or command result")

@command
def summon(entity: EntityId, pos: Coords = None, nbt: EntityNBT = None):
    out = f"summon {entity}"
    if pos:
        out += f" {pos}"
    if nbt:
        out += f" {nbt}"
    return out

@command
def setblock(pos: Coords, block: BlockId, mode: Literal["destroy", "keep", "replace"] = None):
    out = f"setblock {pos} {block}"
    if mode:
        out += f" {mode}"
    return mode

@command
def spawnpoint(targets: Selector, pos: Coords = None, angle: float = None):
    out = f"spawnpoint {targets}"
    if pos:
        out += f" {pos}"
    if angle:
        out += f" {angle}"
    return out


@overload
def spectate(): ...
@overload
def spectate(target: Selector, player: Selector = None): ...

@command
def spectate(target: Selector = None, player: Selector = None):
    if target is None:
        return "spectate"
    
    out = f"spectate {target}"
    if player:
        out += f" {player}"
    
    return out

@command
def spreadplayers(center: Tuple[Coord, Coord], spread_dist: float, max_range: float, respect_teams: bool, targets: Selector):
    return f"spreadplayers {" ".join(center)} {spread_dist} {max_range} {str(respect_teams).lower()} {targets}"

@command
def spreadplayers_under(center: Tuple[Coord, Coord], spread_dist: float, max_range: float, max_height: float, respect_teams: bool, targets: Selector):
    return f"spreadplayers {" ".join(center)} {spread_dist} {max_range} under {max_height} {str(respect_teams).lower()} {targets}"

@command
def fill(from_: Coords, to: Coords, block: BlockId, mode: Literal["destroy", "hollow", "keep", "outline", "replace"] = None):
    out = f"fill {from_} {to} {block}"
    if mode:
        out += f" {mode}"
    return out

#! Commands based on class

class time:
    @command_static
    def add(amount: int):
        return f"time add {amount}"
    
    @command_static
    def query(mode: Literal["daytime", "gametime", "day"]):
        return f"time query {mode}"
    
    @command_static
    def set(time: Literal["day", "night", "noon", "midnight"] | int):
        return f"time set {time}"


class schedule:
    @command_static
    def function(function: MCFunc, time: int, mode: Literal["append", "replace"] = None):
        out = f"schedule function {function} {time}"
        if mode:
            out += f" {mode}"
        return out
    
    @command_static
    def clear(function: MCFunc):
        return f"schedule clear {function}"


class title:
    def __init__(self, targets: Selector):
        self.targets = targets
    
    @command
    def clear(self):
        return f"title {self.targets} clear"
    
    @command
    def reset(self):
        return f"title {self.targets} reset"
    
    @command
    def title(self, text: Text):
        return f"title {self.targets} title {text}"
    
    @command
    def subtitle(self, text: Text):
        return f"title {self.targets} subtitle {text}"
    
    @command
    def actionbar(self, text: Text):
        return f"title {self.targets} actionbar {text}"
    
    @command
    def times(self, fade_in: int, stay: int, fade_out: int):
        return f"title {self.targets} times {fade_in} {stay} {fade_out}"
    

class ride:
    @command_static
    def mount(targets: Selector, vehicle: Selector):
        return f"ride {targets} mount {vehicle}"
    
    @command_static
    def dismount(targets: Selector):
        return f"ride {targets} dismount"


class random:
    @command_static
    def value(range: str, sequence: str = None): # TODO: replace range
        out = f"random value {range}"
        if sequence:
            out += f" {sequence}"
        return out
    
    @command_static
    def roll(range: str, sequence: str = None): # TODO: replace range
        out = f"random roll {range}"
        if sequence:
            out += f" {sequence}"
        return out

    @command_static
    def reset(sequence: Literal["*"] | str, seed: int = None, include_world_seed: bool = None, include_sequence_id: bool = None):
        out = f"random reset {sequence}"
        if seed:
            out += f" {seed}"
        if include_world_seed:
            out += f" {str(include_world_seed).lower()}"
        if include_sequence_id:
            out += f" {str(include_sequence_id).lower()}"
        return out
        

class clone:
    """
    Minecraft `clone` command. Needs initialization. Subcommands:
    
    - `clone().from_()` and `clone().from_().to()` are optional beginings
    - `clone().replace()`
    - `clone().masked()`
    - `clone().filtered()`
    """
    
    def __init__(self, begin: Coords, end: Coords, destination: Coords) -> None:
        self.begin = begin
        self.end = end
        self.destination = destination
        self._from = None
        self._to = None
    
    dimensions = Literal["minecraft:overworld", "minecraft:the_end", "minecraft:the_nether"]
    def from_(self, dimension: dimensions):
        self._from = dimension
        return self
    
    def to(self, dimension: dimensions):
        self._to = dimension
        return self
    
    def _gen_begining(self):
        out = "clone "
        if self._from is not None:
            out += f"from {self._from}"
        out += f"{self.begin} {self.end} "
        if self._to is not None:
            out += f"to {self._to} "
        out += f"{self.destination} "
        return out

    mode = Literal["force", "move", "normal"]
    @command
    def replace(self, mode: mode = "normal"):
        return f"{self._gen_begining()} replace {mode}"
    
    @command
    def masked(self, mode: mode = "normal"):
        return f"{self._gen_begining()} masked {mode}"
    
    @command
    def filtered(self, filter: BlockId, mode: mode = "normal"):
        return f"{self._gen_begining()} filtered {filter} {mode}"


class damage:
    """
    Minecraft `damage` command. Can be used only like `damage()` or with subcommands:
    - `damage.at()`
    - `damage.by()`
    """
    
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

    @command
    def __init__(self, target: Selector, amount: int, damage_type: damage_types = None) -> None:
        @command
        def do():
            if damage_type is None:
                return f"damage {target} {amount}"
            return f"damage {target} {amount} {damage_type}"
        
        do()
    
    @command_static
    def at(target: Selector, amount: int, damage_type: damage_types, location: Coords):
        return f"damage {target} {amount} {damage_type} at {location}"
    
    # @overload
    # def by(target: Selector, amount: int, damage_type: str, by: Selector): ...
    # @overload
    # def by(target: Selector, amount: int, damage_type: str, by: Selector, from_: Selector): ...
    @command_static
    def by(target: Selector, amount: int, damage_type: damage_types, by: Selector, from_: Selector = None):
        if from_ is None:
            return f"damage {target} {amount} {damage_type} by {by}"
        return f"damage {target} {amount} {damage_type} by {by} from {from_}"


class effect:
    """
    Minecraft `effect` command. Subcommands:
    - `effect.clear()`
    - `effect.give()`
    """
    
    @command_static
    def clear(targets: Selector | None = None, effect: EffectId | None = None):
        out = "effect clear"
        if targets is not None:
            out += f" {targets}"
        if effect is not None:
            out += f" {str(effect).strip('"')}"
        return out
    
    @command_static
    def give(targets: Selector, effect: EffectId, seconds: int | Literal["infinite"] | None = None, amplifier: int | None = None, hide_particles: bool | None = None):
        out = f"effect give {targets} {str(effect).strip('"')}"
        if seconds is not None:
            out += f" {seconds}"
        if amplifier is not None:
            out += f" {amplifier}"
        if hide_particles is not None:
            out += f" {str(hide_particles).lower()}"
        return out


class forceload:
    """
    Minecraft `forceload` command. Subcommands:
    - `forceload.add()`
    - `forceload.remove()`
    - `forceload.query()`
    """
    
    @command_static
    def add(from_: Coords, to: Coords | None = None):
        out = f"forceload add {from_}"
        if to is not None:
            out += f" {to}"
        return out
    
    @command_static
    def remove(from_: Coords, to: Coords | None = None):
        out = f"forceload remove {from_}"
        if to is not None:
            out += f" {to}"
        return out
    
    @command_static
    def query(pos: Coords | None):
        if pos:
            return f"forceload query {pos}"
        return "forceload query"


class tag:
    """
    Minecraft `tag` command. Subcommands:
    
    - tag.add()
    - tag.list()
    - tag.remove()
    """
    
    @command_static
    def add(targets: Selector, name: str):
        return f"tag {targets} add {name}"
    
    @command_static
    def list(targets: Selector):
        return f"tag {targets} list"
    
    @command_static
    def remove(targets: Selector, name: str):
        return f"tag {targets} remove {name}"


class tp:
    @overload
    def __init__(self, targets: Selector, destination: Selector): ...
    @overload
    def __init__(self, targets: Selector, location: Coords): ...
    @overload
    def __init__(self, targets: Selector, location: Coords, rotation: Tuple[float, float]): ...
    
    def __init__(self, targets: Selector, destination: Selector | Coords, rotation: Tuple[float, float] = None) -> None:
        @command
        def do():
            self.out = f"tp {targets} {destination if isinstance(destination, Selector) else destination}"
            if rotation is not None:
                self.has_rotation = True
                self.out += f" {rotation}"
            return self.out
        
        do()

    @command
    def facing(self, location: Coords):
        if hasattr(self, "has_rotation"):
            raise RuntimeError("This tp function already defined rotation during main command")
        _cancel_last()
        self.out += f" facing {location}"
        return self.out
    
    @command
    def facing_entity(self, target: Selector, anchor: Literal["eyes", "foot"] = None):
        _cancel_last()
        self.out += f" facing entity {target}"
        if anchor is not None:
            self.out += f" {anchor}"
        return self.out


teleport = tp


class trigger:
    """
    Minecraft `trigger` command. You can use it directly or also apply subcommands:
    - trigger().add()
    - trigger().set()
    """
    
    def __init__(self, objective: ScoreBoard | str) -> None:
        self.objective = objective
        @command
        def do():
            return f"trigger {objective}"
        
        do()
    
    @command
    def add(self, value: int):
        _cancel_last()
        return f"trigger {self.objective} add {value}"
    
    @command
    def set(self, value: int):
        _cancel_last()
        return f"trigger {self.objective} set {value}"


class xp:
    """
    Minecraft `xp` command. Subcommands:
    - `xp.add()`
    - `xp.set()`
    - `xp.query()`
    """
    
    @command_static
    def add(target: Selector, amount: int, type_: Literal["levels", "points"]):
        return f"xp add {target} {amount} {type_}"
    
    @command_static
    def set(target: Selector, amount: int, type_: Literal["levels", "points"]):
        return f"xp set {target} {amount} {type_}"
    
    @command_static
    def query(target: Selector, type_: Literal["levels", "points"]):
        return f"xp query {target} {type_}"

experience = xp


#! Importing complex commands from their modules

from .scoreboard import *
from .execute import *
from .bossbar import *
from .attribute import *
from .item import *
from .sound import *
from .particle import *
from .team import *
from .data import *
