from typing import Literal
from .decorators import command, command_static
from structures import Text, Selector

__all__ = ["Team", "team"]
do_command = True

class Team:
    def __init__(self, name: str, display_name: Text = None) -> None:
        global do_command
        self.name = name
        self.display_name = display_name
        if do_command:
            team.add(name, display_name)
        self._color = "reset"
        self._friendly_fire = True
        self._see_friendly_invisibles = True
        self._nametag_visibility = "always"
        self._death_message_visibility = "always"
        self._collision_rule = "always"
        self._prefix = ""
        self._suffix = ""
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def display_name(self, display_name: Text):
        return f"team modify {self.team} displayName {display_name}"
    
    colors = Literal["blue", "green", "pink", "purple", "red", "white", "yellow", "aqua", "black", "dark_aqua", "dark_blue", "dark_gray", "dark_green", "dark_purple", "dark_red", "gold", "gray", "light_purple", "reset"]
    @property
    def color(self):
        return self._color
    
    @property
    def friendly_fire(self):
        return self._friendly_fire
    
    @property
    def see_friendly_invisibles(self):
        return self._see_friendly_invisibles
    
    @property
    def nametag_visibility(self):
        return self._nametag_visibility
    
    @property
    def death_message_visibility(self):
        return self._death_message_visibility
    
    @property
    def collision_rule(self):
        return self._collision_rule
    
    @property
    def prefix(self):
        return self._prefix
    
    @property
    def suffix(self, text: Text):
        return self._suffix
    
    @color.setter
    def color(self, val):
        team.modify(self.name).color(val)

    @friendly_fire.setter
    def friendly_fire(self, val):
        team.modify(self.name).friendly_fire(val)

    @see_friendly_invisibles.setter
    def see_friendly_invisibles(self, val):
        team.modify(self.name).see_friendly_invisibles(val)

    @nametag_visibility.setter
    def nametag_visibility(self, val):
        team.modify(self.name).nametag_visibility(val)

    @death_message_visibility.setter
    def death_message_visibility(self, val):
        team.modify(self.name).death_message_visibility(val)

    @collision_rule.setter
    def collision_rule(self, val):
        team.modify(self.name).collision_rule(val)

    @prefix.setter
    def prefix(self, val):
        team.modify(self.name).prefix(val)

    @suffix.setter
    def suffix(self, val):
        team.modify(self.name).suffix(val)

    
class team_modify:
    def __init__(self, team: Team | str) -> None:
        self.team = team
    
    @command
    def display_name(self, display_name: Text):
        return f"team modify {self.team} displayName {display_name}"
    
    colors = Literal["blue", "green", "pink", "purple", "red", "white", "yellow", "aqua", "black", "dark_aqua", "dark_blue", "dark_gray", "dark_green", "dark_purple", "dark_red", "gold", "gray", "light_purple", "reset"]
    @command
    def color(self, color: colors):
        return f"team modify {self.team} color {color}"
    
    @command
    def friendly_fire(self, allowed: bool):
        return f"team modify {self.team} friendlyFire {str(allowed).lower()}"
    
    @command
    def see_friendly_invisibles(self, allowed: bool):
        return f"team modify {self.team} seeFriendlyInvisibles {str(allowed).lower()}"
    
    @command
    def nametag_visibility(self, mode: Literal["never", "hideForOtherTeams", "hideForOwnTeam", "always"]):
        return f"team modify {self.team} nametagVisibility {mode}"
    
    @command
    def death_message_visibility(self, mode: Literal["never", "hideForOtherTeams", "hideForOwnTeam", "always"]):
        return f"team modify {self.team} deathMessageVisibility {mode}"
    
    @command
    def collision_rule(self, mode: Literal["always", "never", "pushOtherTeams", "pushOwnTeam"]):
        return f"team modify {self.team} collisionRule {mode}"
    
    @command
    def prefix(self, text: Text):
        return f"team modify {self.team} prefix {text}"
    
    @command
    def suffix(self, text: Text):
        return f"team modify {self.team} suffix {text}"


class team:
    @command_static
    def list(team: Team | str = None):
        out = f"team list"
        if team:
            out += f" {team}"
        return out
    
    def add(name: str, display_name: Text = None) -> Team:
        global do_command
        do_command = False
        
        @command
        def do():
            out = f"team add {name}"
            if display_name:
                out += f" {display_name}"
            return out
        
        do()

        t = Team(name, display_name)
        do_command = True
        
        return t
    
    @command_static
    def remove(team: Team | str):
        return f"team remove {team}"
    
    @command_static
    def empty(team: Team | str):
        return f"team empty {team}"
    
    @command_static
    def join(team: Team | str, members: Selector):
        return f"team join {team} {members}"
    
    @command_static
    def leave(members: Selector):
        return f"team leave {members}"
    
    def modify(team: Team | str) -> team_modify:
        return team_modify(team)
