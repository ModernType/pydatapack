"""Scoreboard command implementation"""
from typing import Literal
from structures.text import Text
from structures.enums import SetdisplayVars
from structures.entity import Selector
from .decorators import command

__all__ = ["ScoreBoard", "scoreboard"]

class ScoreBoard:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def displayname(self):
        return self.name
    
    @displayname.setter
    def displayname(self, val: Text | str):
        scoreboard.objectives.modify(self.name, "displayname", val)
    
    def setdisplay(self, display: SetdisplayVars):
        scoreboard.objectives.setdisplay(display, self)
    
    @command
    def add(self, selector: Selector, score: int):
        return _ScoreboardPlayers.add(selector, self, score)
    
    @command
    def enable(self, targets: Selector):
        return _ScoreboardPlayers.PREFIX + f"enabel {targets} {self}"
    
    @command
    def get(self, selector: Selector | str):
        return _ScoreboardPlayers.PREFIX + f"get {selector} {self}"
    
    @command
    def remove(self, selector: Selector | str, score: int):
        return _ScoreboardPlayers.PREFIX + f"remove {selector} {self} {score}"
    
    @command
    def reset(self, selector: Selector | str):
        return _ScoreboardPlayers.PREFIX + f"reset {selector} {self}"
    
    @command
    def set(self, selector: Selector | str, score: int):
        return _ScoreboardPlayers.PREFIX + f"set {selector} {self} {score}"


class _ScoreboardObjectives:
    PREFIX = "scoreboard objectives "

    @staticmethod
    def add(objective: str, criteria: str, display_name: Text | str = None) -> ScoreBoard:
        @command
        def do_command():
            if display_name is None:
                return _ScoreboardObjectives.PREFIX + f"add {objective} {criteria}"
            return _ScoreboardObjectives.PREFIX + f"add {objective} {criteria} {display_name}"

        do_command()
        return ScoreBoard(objective)

    @staticmethod
    @command
    def list():
        return _ScoreboardObjectives.PREFIX + "list"

    modifies = Literal["displayname", "rendertype"]
    @staticmethod
    @command
    def modify(objective: ScoreBoard | str, parameter: modifies, value: Text | str):
        return _ScoreboardObjectives.PREFIX + f"modify {objective} {parameter} {value}"

    @staticmethod
    @command
    def remove(objective: ScoreBoard | str):
        command = _ScoreboardObjectives.PREFIX + f"remove {objective}"
        if isinstance(objective, ScoreBoard):
            del objective
        return command

    @staticmethod
    @command
    def setdisplay(display: SetdisplayVars | str, objective: ScoreBoard | str):
        return _ScoreboardObjectives.PREFIX + f"setdisplay {display} {objective}"

class _ScoreboardPlayers:
    PREFIX = "scoreboard players "

    @staticmethod
    @command
    def add(selector: Selector | str, objective: ScoreBoard | str, score: int):
        return _ScoreboardPlayers.PREFIX + f"add {selector} {objective} {score}"
    
    @staticmethod
    @command
    def enable(targets: Selector, objective: ScoreBoard | str):
        return _ScoreboardPlayers.PREFIX + f"enabel {targets} {objective}"
    
    @staticmethod
    @command
    def get(selector: Selector | str, objective: ScoreBoard | str):
        return _ScoreboardPlayers.PREFIX + f"get {selector} {objective}"
    
    @staticmethod
    @command
    def list(selector: Selector | str):
        return _ScoreboardPlayers.PREFIX + f"list {selector}"
    
    operation = Literal["%=", "*=", "+=", "-=", "/=", "<", "=", ">", "><"]
    @staticmethod
    @command
    def operation(target: Selector | str,
                  target_obj: ScoreBoard | str,
                  operation: operation,
                  source: Selector | str,
                  source_obj: ScoreBoard | str):
        return _ScoreboardPlayers.PREFIX + f"operation {target} {target_obj} {operation} {source} {source_obj}"
    
    @staticmethod
    @command
    def remove(selector: Selector | str, objective: ScoreBoard | str, score: int):
        return _ScoreboardPlayers.PREFIX + f"remove {selector} {objective} {score}"
    
    @staticmethod
    @command
    def reset(selector: Selector | str, objective: ScoreBoard | str | None = None):
        if objective is None:
            return _ScoreboardPlayers.PREFIX + f"reset {selector}"
        return _ScoreboardPlayers.PREFIX + f"reset {selector} {objective}"
    
    @staticmethod
    @command
    def set(selector: Selector | str, objective: ScoreBoard | str, score: int):
        return _ScoreboardPlayers.PREFIX + f"set {selector} {objective} {score}"


class scoreboard:
    objectives = _ScoreboardObjectives
    players = _ScoreboardPlayers


if __name__ == "__main__":
    from commands import mc_function, say

    @mc_function(log=True)
    def test():
        some: ScoreBoard = scoreboard.objectives.add("some", "dummy")
        some.setdisplay(SetdisplayVars.sidebar)
        scoreboard.players.add(Selector("@a", sort="nearest", limit=1), some, 5)
        say("Scoreboard test finished")
