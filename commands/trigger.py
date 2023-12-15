from .decorators import command, _cancel_last
from .scoreboard import ScoreBoard

__all__ = ["trigger"]


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
