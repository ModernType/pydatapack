from structures.enums import *
from structures.text import Text
from structures.commands import mc_function, give
from structures.general import AttributeModifier
from structures.item import Item, Enchantment, Display
from core import NameSpace

# print(Enchantment(EnchantmentId.looting))
# print(Text("[b]Good[/b] Morning"))

foo = Item("minecraft:diamond_sword", attribute_modifiers=[AttributeModifier(AttributeName.attack_damage, amount=7), AttributeModifier(AttributeName.attack_speed, amount=-2.6)], enchantments=[Enchantment(EnchantmentId.mending)], unbreakable=True, hide_flags=HideFlags.attributes+HideFlags.unbreakable,
           display=Display(Text("[color=orange][b]Special Sword"), Text("[i]Cool lore[/i]\n[color=gold]For [b]cool[/b] item")))

@mc_function
def test():
    give(foo)

print(test())