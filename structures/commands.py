from typing import Callable, List
from .item import Item
from core import NameSpace

fun_buf: List[str] = []


def mc_function(func: Callable = None, namespace: NameSpace = None, func_name: str = None):
    """Decorator to define python function as minecraft function"""

    def inner(func):
        def wrapper(*args, **kwargs):
            global fun_buf
            func(*args, **kwargs)
            return "\n".join(fun_buf)
    
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

    if namespace or func_name:
        return inner
    return inner(func)


def base_command(func: Callable[[], str]):
    def wrapper(*args, **kwargs):
        global fun_buf
        fun_buf.append(func(*args, **kwargs))

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__annotations__ = func.__annotations__
    return wrapper


@base_command
def give(item: Item, player: str = "@s"):
    return f"give {player} {item.give_string()}"


@base_command
def say(text: str):
    return f"say {text}"



if __name__ == "__main__":

    @mc_function
    def test():
        give()
        give("@s")
    
    print(test())
    print(test.__mc__)

