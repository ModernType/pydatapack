from typing import List, Callable, Iterable
from core import NameSpace #! Potentialy can couse circular import

__all__ = ["mc_function", "command_macro"]

fun_buf: List[str] = []

def mc_function(func: Callable = None, /, *, namespace: NameSpace = None, func_name: str = None, log: bool = False):
    """Decorator to define python function as minecraft function

    Args:
        namespace (NameSpace, optional): Namesspace which will be assigned to this function. You won't need to use add_function() method later.
        func_name (str, optional): Name of function file. If not present original function name will be used.
    """

    def inner(func):
        def wrapper(*args, **kwargs):
            global fun_buf
            func(*args, **kwargs)
            return "\n".join(fun_buf)

        if log:
            print(wrapper())

        if func_name:
            wrapper.__name__ = func_name
        else:
            wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__annotations__ = func.__annotations__
        wrapper.__mc__ = True
        if namespace:
            wrapper.__namespace__ = namespace
            namespace.add_function(wrapper)
        if not hasattr(wrapper, "__namespace__"):
            wrapper.__namespace__ = None
        return wrapper

    if not func:
        return inner
    return inner(func)


def command_macro(func: Callable[[], str]):
    """Decorator to define function's return string as minecraft command. You will be able to use this function
    inside `@mc_function` decorated functions as a standalone minecraft command. This decorator is used
    for every builtin command in this library.
    You should treat decorated functions as macros for generating strings with minecraft commands.

    Example:
    ```
    @command_macro
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


def _cancel_last():
    global fun_buf
    fun_buf.pop()
