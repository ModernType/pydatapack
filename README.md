# PyDatapack (still working on name)

Python framework to pythonize process of minecraft datapacks creation.

## How to start

All you need is to place at the begining of your script:

```python
from pydatapack import *
```

Then you need to create an instance of your datapack and at least one namespace:

```python
datapack = DataPack()

dp = NameSpace("dp")
```

After that you can start defining your minecraft functions. To do this you should decorate
standard python function with `@mc_function` decorator like so:

```python
@mc_function
def foo():
    give(Item(ItemId.diamond_sword))
```

To add minecraft function to namespace you need to write afterwards:

```python
dp.add_function(foo)
```

Or define it directly in `@mc_function`:

```python
@mc_function(namespace=dp)
def foo(): ...
```

## Using `execute` command

`execute` command is special because in minecraft you can chain it infinitely until you close it with `run` subcommand. In this farmework you can do it in the same way.

### Example

```python
@mc_function(namespace=dp, log=True)
def execute_showcase():
    execute()\
        .as_(Selector(
            SelectorEnum.all_players,
            tag="special"
            ))\
        .run(
            give(Item(
                ItemId.diamond_sword,
                display=Display(
                    name=Text("[b]Cool sword")
                )
            ))
        )
```

### Output

`
execute_showcase:
    execute as @a[tag=special] run give @s minecraft:diamond_sword{display:{Name:'{"text":"Cool sword","bold":"true","italic":"false"}'}} 1
`

> Note: if you forget to end `execute` command with `run` the whole command will be skipped, no error will be occured

## Creating groups of commands

If you have some block of commands with small changes, you can create function decorated with `@command_macro`, so it will be treated as regular command but will yield a few ones based on arguments.

### Example

```python
@command_macro
def give_to_special(item: Item):
    execute().as_(Selector(SelectorEnum.all_players, tag="special")).run(
        give(item)
    )
    say(f"Gave {item}")

@mc_function
def foo():
    give_to_special(Item(ItemId.diamond_sword))
    give_to_special(Item(ItemId.command_block))
```

Or you can use it with `for` loop:

```python
@command_macro
def test_slot(slot_num: int):
    execute()\
        .as_("@a")\
        .if_().entity(Selector(
            SelectorEnum.executor,
            nbt=EntityNBT(
                Inventory=[
                    {
                        "Slot": slot_num,
                        "id": "minecraft:diamond"
                    }
                ]
            )
        ))\
        .run(
            say(f"Some player has diamond in slot {slot_num}")
        )

@mc_function(namespace=dp, log=True)
def test_slot_function():
    for i in range(11):
        test_slot(i)
```
