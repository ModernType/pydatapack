from .decorators import command
from structures.entity import Selector
from structures.enums import EffectId
from typing import Literal

__all__ = ["effect"]


class effect:
    @staticmethod
    @command
    def clear(targets: Selector | None = None, effect: EffectId | None = None):
        out = "effect clear"
        if targets is not None:
            out += f" {targets}"
        if effect is not None:
            out += f" {str(effect).strip('"')}"
        return out
    
    @staticmethod
    @command
    def give(targets: Selector, effect: EffectId, seconds: int | Literal["infinite"] | None = None, amplifier: int | None = None, hide_particles: bool | None = None):
        out = f"effect give {targets} {str(effect).strip('"')}"
        if seconds is not None:
            out += f" {seconds}"
        if amplifier is not None:
            out += f" {amplifier}"
        if hide_particles is not None:
            out += f" {str(hide_particles).lower()}"
        return out
