from typing import List, Callable

__all__ = ["command","command_static" , "command_macro"]

fun_buf: List[str] = []


def command_macro(func: Callable[[], str]):
    """ Function decorated with `command_macro` acts like "inline" minecraft function.
    
    ## Example
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
    """
    def wrapper(*args, **kwargs):
        global fun_buf
        func(*args, **kwargs)
        out = "\n".join(fun_buf)
        fun_buf.clear()
        return out

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__annotations__ = func.__annotations__
    return wrapper


def command(func: Callable[[], str]):
    """Decorator to define function's return string as minecraft command. You will be able to use this function
    inside `@mc_function` decorated functions as a standalone minecraft command. This decorator is used
    for every builtin command in this library.
    You should treat decorated functions as macros for generating strings with minecraft commands.

    ## Example
    ```
    @command
    def give(item: Item, player: str = "@s"):
        return f"give {player} {item.give_string()}"
    ```
    And then you can use it:
    ```
    @mc_function
    def foo():
        give(Item(ItemId.diamond))
    ```
    which will result in file `foo.mcfunction` with content:
    `give @s minecraft:diamond`
    """
    
    def wrapper(*args, **kwargs):
        global fun_buf
        command = func(*args, **kwargs)
        fun_buf.append(command)
        return command

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__annotations__ = func.__annotations__
    return wrapper


def command_static(func: Callable[[], str]):
    """This decorator combines effects of `@staticmethod` and `@command` decorators functions.

    ## Example
    Code block below:
    ```
    class forceload:
        @staticmethod
        @command
        def add(from_: Coords, to: Coords | None = None): ...
    ```
    can be replaced with one decorator:
    ```
    class forceload:
        @command_static
        def add(from_: Coords, to: Coords | None = None): ...
    ```
    """

    @staticmethod
    def wrapper(*args, **kwargs):
        global fun_buf
        command = func(*args, **kwargs)
        fun_buf.append(command)
        return command

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__annotations__ = func.__annotations__
    return wrapper


def _cancel_last():
    global fun_buf
    fun_buf.pop()
