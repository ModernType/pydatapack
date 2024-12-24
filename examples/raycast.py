from pydatapack import *

rc_dist = ScoreBoard("rc_dist")

@command_macro
def raycast_recursive(recursive_func_name: str, final_func: MCFunc, display_particle: Particle | None = None, rc_distance: int = 16, rc_step: int = 0.5):
    rc_dist.add("@s", 1)
    if display_particle:
        particle(display_particle, Coords("~ ~ ~"), Coords("0 0 0"), 0, 1, "force")
    execute().unless().block(Coords("~ ~ ~"), "minecraft:air")\
        .as_(Selector(
            "@s",
            score=f"{{rc_dist=..{int(rc_distance * 2 / rc_step)}}}"
        ))\
        .positioned(Coords(f"^ ^ ^-{rc_step}"))\
        .run(final_func())
    execute().positioned(Coords("~ ~-1 ~"))\
        .if_().entity(Selector(
            "@e",
            distance="..1",
            tag="!rc"
        ))\
        .positioned(Coords("~ ~1 ~"))\
        .run(final_func())
    execute().as_(Selector("@s", score=f"{{rc_dist={int(rc_distance * 2 / rc_step)}}}"))\
        .positioned(f"^ ^ ^-{rc_step}")\
        .run(final_func())
    
    execute().if_().block("~ ~ ~", "minecraft:air")\
        .as_(Selector(score=f"{{rc_dist=..{int(rc_distance * 2 / rc_step)}}}"))\
        .positioned("~ ~-1 ~")\
        .unless().entity(Selector(
            "@e",
            distance="..1",
            tag="!rc"
        ))\
        .positioned("~ ~1 ~")\
        .positioned(f"^ ^ ^{rc_step}")\
        .run(
            raw_command(f"function pydp:raycast/{recursive_func_name}")
        )

@command_macro
def raycast_start(recursive_func: MCFunc):
    tag.add("@s", "rc")
    rc_dist.set("@s", 0)
    execute().at("@s").anchored("eyes").positioned(Coords("^ ^ ^0.5")).run(
        recursive_func()
    )


def create_raycast_function(func_name: str, final_func: MCFunc, rc_particle: Particle = None, rc_distance: int = 16, rc_step: int = 0.5) -> MCFunc:
    """Use this function to crate raycast function with specified parameters.

    Parameters:
    - `func_name` - name of raycast starting function
    - `final_func` - func to run when ray hits target
    - `rc_particle` - particles to display while raycasting
    - `rc_distance` - max distance the ray can travel
    - `rc_step` - step distance. Less is more precise but more performance heavy
    """
    @mc_function(func_name=f"{func_name}_recursive", path="raycast")
    def recursive():
        raycast_recursive(f"{func_name}_recursive", final_func, rc_particle, rc_distance, rc_step)
    
    @mc_function(func_name=func_name, path="raycast")
    def main():
        raycast_start(recursive)
    
    return main
