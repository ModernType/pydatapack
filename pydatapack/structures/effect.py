from .enums import *

class Effect:
    def __init__(self,
                 id: EffectId,
                 duration: int = 60,
                 amplifier: int = 0,
                 hide_particles: bool = False
                 ) -> None:
        self.id = id
        self.duration = duration
        self.amplifier = amplifier
        self.hide_particles = hide_particles
