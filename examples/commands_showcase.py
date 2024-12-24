from pydatapack import *

datapack = DataPack()
test_team = Team("test")
test_team.color = "red"
rmb = ScoreBoard("rmb")
bar = BossBar("test", Text("Test"))
bar.style = "notched_10"

@mc_function(log=True)
def foo():
    some = scoreboard.objectives.add("some", "dummy")
    player = Selector("ModernTy")
    xp.set(player, 5, "levels")
    some.set(player, 5)
    execute().as_(player).if_().score(Selector(), some, "matches", "..10").store("result").score(Selector(), some).run(scoreboard.players.get(Selector(), some))
    execute().as_(player).store("result").score(Selector(), some).run(clear(Selector(), Item(ItemId.diamond, tags=["special"]), 0))
    damage.by(player, 5, "minecraft:generic", Selector())
    effect.give(player, EffectId.hunger)
    effect.clear(player)
    forceload.add(Coords("~ ~ ~"))
    # clear(player, Item(ItemId.diamond_sword))
    # execute().as_(player).if_().score(Selector(), some, "matches", "5..").run(give(Item(ItemId.diamond_sword)))
    # execute().at(player).summon(EntityId.zombie).run(say(5))


@mc_function(log=True)
def sound_test():
    playsound("entity.enderman.ambient", "master", Selector(), Coords("~ ~ ~"), 6, 1, 2)
    title(Selector()).actionbar(Text("[b]Test text"))
    gamerule("keepInventory", True)

@tick
@mc_function(log=True)
def main():
    foo()

datapack.generate()
