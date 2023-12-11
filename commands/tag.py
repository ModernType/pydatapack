from .decorators import command_static
from structures.entity import Selector

__all__ = ["tag"]


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
