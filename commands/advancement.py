from .decorators import command
from structures import Selector

__all__ = ["advancement"]


class advancement_options:
    def __init__(self, cur_com) -> None:
        self.cur_com = cur_com
    
    @command
    def everything(self):
        return f"{self.cur_com} everything"
    
    @command
    def only(self, advancement: str, criterion: str = None):
        out = f"{self.cur_com} only {advancement}"
        if criterion:
            out += f" {criterion}"
        return out
    
    @command
    def from_(self, advancement: str):
        return f"{self.cur_com} from {advancement}"
    
    @command
    def through(self, advancement: str):
        return f"{self.cur_com} through {advancement}"
    
    @command
    def until(self, advancement: str):
        return f"{self.cur_com} until {advancement}"


class advancement:
    @staticmethod
    def grant(targets: Selector) -> advancement_options:
        return advancement_options(f"advancement grant {targets}")
    
    @staticmethod
    def revoke(targets: Selector) -> advancement_options:
        return advancement_options(f"advancement revoke {targets}")
