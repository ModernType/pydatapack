from __future__ import annotations
from .enums import MCEnum
from .enums import *
from typing import List, overload, Any
import random

def to_camel_case(s: str):
    res = s.split("_")
    res = list(map(lambda x: x.title(), res))
    return "".join(res)

def prettify(v: Any):
    if isinstance(v, str):
        return f"{v}"
    elif isinstance(v, bool):
        return f'{int(v)}b'
    elif isinstance(v, list):
        return f"[{", ".join(map(prettify, v))}]"
    elif isinstance(v, dict):
        buf = []
        for k, v in v.items():
            buf.append(f"{k}:{prettify(v)}")
        return "{" + ", ".join(buf) + "}"
    elif isinstance(v, int):
        if v < 256:
            return f"{v}b"
        else:
            return str(v)
    else:
        return str(v)

class TagClass:
    """Class to be inherited from to automaticaly implement __str__ method of class in a way necessary for commands to proceed correctly"""
    quoted_key: bool = False # defines if key value of class should be in quotes

    do_camel_case: bool = True # defines if needed to convert class keys to camel case
    
    exceptions: set = set() # a set of keys which won't be affected with `do_camel_case`
    
    ignore: set = set() # a set of service attributes to not include into command creation

    def __str__(self) -> str:
        additions = []

        for k, v in self.__dict__.items():
            if k in self.ignore:
                continue
            
            key = f'"{k}"' if self.quoted_key and k not in self.exceptions else k
            if self.do_camel_case and k not in self.exceptions: key = to_camel_case(key)

            if v is None:
                continue
            else:
                additions.append(f"{key}:{prettify(v)}")
        
        res = ",".join(additions)

        return f"{{{res}}}"

    def __repr__(self) -> str:
        return self.__str__()


class UUID:
    def __init__(self, i1: int = None, i2: int = None, i3: int = None, i4: int = None) -> None:
        i1 = i1 if i1 is not None else random.randint(0, 2147483648)
        i2 = i2 if i2 is not None else random.randint(0, 2147483648)
        i3 = i3 if i3 is not None else random.randint(0, 2147483648)
        i4 = i4 if i4 is not None else random.randint(0, 2147483648)

        self.l = [i1, i2, i3, i4]
    
    def __str__(self) -> str:
        return "[I;" + str(self.l)[1:]

    def __repr__(self) -> str:
        return self.__str__()


class AttributeModifier(TagClass):
    def __init__(self,
                 attribute_name: str,
                 slot: str = Slot.mainhand,
                 operation: int = AttributeOperation.add,
                 amount: float = 0,
                 name: str = None,
                 uuid: UUID = None
                 ) -> None:
        self.attribute_name = attribute_name
        self.name = name if name is not None else attribute_name
        self.slot = slot
        self.operation = operation
        self.amount = amount
        self.uuid = uuid if uuid is not None else UUID()


class CoordinateType(MCEnum):
    absolute = ""
    relative = "~"
    sight = "^"
    
    def __str__(self) -> str:
        return self.without_quotes()


class Coord:
    def __init__(self, coord: float = 0, coord_type: CoordinateType = CoordinateType.absolute) -> None:
        self.coord = coord
        self.coord_type = coord_type
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return f"{self.coord_type}{self.coord}"

    @classmethod
    def make_from(cls, inp: Coord | float | str) -> Coord:
        if isinstance(inp, Coord):
            return inp
        elif isinstance(inp, float):
            return cls(inp)
        elif isinstance(inp, str):
            match inp[0]:
                case "~":
                    try:
                        return cls(float(inp[1:]), CoordinateType.relative)
                    except ValueError:
                        return cls(0, CoordinateType.relative)
                case "^":
                    try:
                        return cls(float(inp[1:]), CoordinateType.sight)
                    except ValueError:
                        return cls(0, CoordinateType.sight)
                case _:
                    try:
                        return cls(float(inp), CoordinateType.absolute)
                    except ValueError:
                        return cls(0, CoordinateType.absolute)
        else:
            raise TypeError("You should pass Coord, float or str type")


class Coords:
    @overload
    def __init__(self, full_coords: str): ...
    @overload
    def __init__(self, x: str, y: str, z: str): ...
    @overload
    def __init__(self, x: Coord, y: Coord, z: Coord): ...
    
    def __init__(self, *args):
        if len(args) == 1:
            args = args[0].split()
        if len(args) == 3:
            self.coords = []
            for i in args:
                self.coords.append(Coord.make_from(i))
        else:
            raise RuntimeError("")
    
    def __str__(self) -> str:
        return f"{self.coords[0]} {self.coords[1]} {self.coords[2]}"
    
    def __repr__(self) -> str:
        return self.__str__()


class Storage:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def __str__(self) -> str:
        if ":" in self.name:
            return self.name
        else:
            return f"minecraft:{self.name}"
    
    def __repr__(self) -> str:
        return self.__str__()
