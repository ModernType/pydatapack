from __future__ import annotations
from .enums import *
from typing import List
import random

def to_camel_case(s: str):
    res = s.split("_")
    res = list(map(lambda x: x.title(), res))
    return "".join(res)

class TagClass:
    """Class to be inherited from to automaticaly implement __str__ method of class in a way necessary for commands to proceed correctly"""
    quoted_key: bool = False # defines if key value of class should be in quotes

    do_camel_case: bool = True # defines if needed to convert class keys to camel case

    def __str__(self) -> str:
        additions = []

        for k, v in self.__dict__.items():
            key = f'"{k}"' if self.quoted_key else k
            if self.do_camel_case: key = to_camel_case(key)

            if v is None:
                continue
            elif isinstance(v, str):
                additions.append(f'{key}:"{v}"')
            elif isinstance(v, bool):
                additions.append(f'{key}:{int(v)}b')
            else:
                additions.append(f'{key}:{v}')
        
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


class Coord:
    def __init__(self, coord: float = 0, coord_type: CoordinateType = CoordinateType.relative) -> None:
        self.coord = coord
        self.coord_type = coord_type
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return f"{self.coord_type}{self.coord}"

    @staticmethod
    def make_from(cls, inp: Coord | float | str) -> Coord:
        if isinstance(inp, Coord):
            return inp
        elif isinstance(inp, float):
            return cls(inp)
        elif isinstance(inp, str):
            match inp[0]:
                case "~":
                    cls(float(inp[1:]), CoordinateType.relative)
                case "^":
                    cls(float(inp[1:]), CoordinateType.sight)
                case _:
                    cls(float(inp), CoordinateType.absolute)
        else:
            raise TypeError("You should pass Coord, float or str type")



