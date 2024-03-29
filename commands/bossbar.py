from .decorators import command, command_static
from structures.text import Text
from typing import Literal
from structures.entity import Selector

__all__ = ["BossBar", "bossbar"]
do_command = True


class BossBar:
    """
    Object for `bossbar` result abstraction. You can call methods of this object to apply `bossbar modify`
    to this bossbar specifically.
    """
    
    def __init__(self, id_: str, name: Text | str) -> None:
        global do_command
        self.id_ = id_
        if do_command:
            bossbar.add(id_, name)
        self._name = name
        self._max = 100
        self._players = None
        self._value = 0
        self._visible = True
    
    @property
    def name(self):
        raise ValueError("You can't get this property")
    
    @name.setter
    def name(self, new: Text | str):
        bossbar.set(self).name(new)
        self._name = new
    
    @property
    def max(self):
        bossbar.get(self, "max")
    
    @max.setter
    def max(self, new: int):
        bossbar.set(self).max(new)
        self._max = new
    
    @property
    def value(self):
        bossbar.get(self, "value")
    
    @value.setter
    def value(self, new: int):
        bossbar.set(self).value(new)
        self._value = new
    
    @property
    def visible(self):
        bossbar.get(self, "visible")
    
    @visible.setter
    def visible(self, new: bool):
        bossbar.set(self).visible(new)
        self._visible = new
    
    @property
    def players(self):
        if self._players is None:
            raise ValueError("No players defined for this bossbar")
        bossbar.get(self, "players")
    
    @players.setter
    def players(self, new: Selector):
        bossbar.set(self).players(new)
        self._players = new

    @property
    def color(self):
        raise ValueError("You can't get this property")
    
    @color.setter
    def color(self, value: Literal["blue", "green", "pink", "purple", "red", "white", "yellow"]):
        bossbar.set(self).color(value)
    
    @property
    def style(self):
        raise ValueError("You can't get this property")
    
    @style.setter
    def style(self, value: Literal["notched_6", "notched_10", "notched_12", "notched_20", "progress"]):
        bossbar.set(self).style(value)
    


    def __str__(self):
        return f"minecraft:{self.id_}"
    
    def __repr__(self) -> str:
        return self.__str__()


class bossbar_set:
    def __init__(self, id_: str) -> None:
        self.id_ = id_
    
    colors = Literal["blue", "green", "pink", "purple", "red", "white", "yellow"]
    @command
    def color(self, color: colors):
        return f"bossbar set {self.id_} color {color}"
    
    @command
    def max(self, max_: int):
        return f"bossbar set {self.id_} max {max_}"
    
    @command
    def name(self, name: Text | str):
        return f"bossbar set {self.id_} name {name}"
    
    @command
    def players(self, target: Selector):
        return f"bossbar set {self.id_} players {target}"
    
    styles = Literal["notched_6", "notched_10", "notched_12", "notched_20", "progress"]
    @command
    def style(self, style: styles):
        return f"bossbar set {self.id_} style {style}"
    
    @command
    def value(self, value: int):
        return f"bossbar set {self.id_} value {value}"
    
    @command
    def visible(self, visible: bool):
        return f"bossbar set {self.id_} visible {str(visible).lower()}"


class bossbar:
    """
    Minecraft `bossbar` command. Subcommands:
    
    - `bossbar.add()` (returns `BossBar` object instance)
    - `bossbar.get()`
    - `bossbar.list()`
    - `bossbar.remove()`
    - `bossbar.set()` (has subcommands)
    
    """
    
    @staticmethod
    def add(id_: str, name: Text | str = None) -> BossBar:
        global do_command
        do_command = False

        @command
        def do():
            if name is None:
                return f"bossbar add {id_}"
            return f"bossbar add {id_} {name}"
        
        do()
        out = BossBar(id_, name)
        do_command = True
        return out
    
    @command_static
    def get(id_: BossBar | str, option: Literal["max", "players", "value", "visible"]):
        return f"bossbar get {id_} {option}"
    
    @command_static
    def list():
        return f"bossbar list"
    
    @command_static
    def remove(id_: BossBar | str):
        return f"bossbar remove {id_}"
    
    @staticmethod
    def set(id_: BossBar | str) -> bossbar_set:
        return bossbar_set(str(id_))