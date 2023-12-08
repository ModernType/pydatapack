from __future__ import annotations
from typing import Any, Callable
from commands.decorators import command
import commands.decorators

LATEST_FORMAT = 15


class MCFunc:
    gen_func: Callable
    namespace: NameSpace
    name: str
    
    def __init__(self, gen_func: Callable, name = None) -> None:
        self.gen_func = gen_func
        self.namespace = []
        self.name = name if name is not None else gen_func.__name__
    
    @command
    def __call__(self) -> Any:
        if self.namespace:
            return f"function {self.namespace}:{self.name}"
        raise RuntimeError("You can't call mc_function without namespace defined")
    
    def _add_namespace(self, namespace: NameSpace):
        self.namespace.append(namespace)
    

def mc_function(func: Callable = None, /, *, namespace: NameSpace = None, func_name: str = None, log: bool = False):
    """One of key decorators which is used to define python function as minecraft function.
    
    ## Example
    Snippet below shows how to create function `foo` inside namespace `dp`
    ```
    dp = NameSpace("dp")
    
    @mc_function
    def foo():
        give(Item(ItemId.diamond))
    
    dp.add_function(foo)
    ```
    or you can do it like this:
    ```
    dp = NameSpace("dp")
    
    @mc_function(namespace=dp)
    def foo():
        give(Item(ItemId.diamond))
    ```
    
    which will result in file `foo.mcfunction` with content:
    `give @s minecraft:diamond`
    """

    def inner(func):
        nonlocal func_name, namespace, log
        
        def gen_func(*args, **kwargs):
            func(*args, **kwargs)
            out = "\n".join(commands.decorators.fun_buf)
            commands.decorators.fun_buf.clear()
            return out

        if log:
            print(f"{func_name if func_name else func.__name__}:\n\t{"\n\t".join(gen_func().splitlines())}")
        
        mc_func = MCFunc(gen_func, func_name if func_name else func.__name__)
        
        if namespace:
            namespace.add_function(mc_func)
        
        return mc_func

    if not func:
        return inner
    return inner(func)


class NameSpace:
    def __init__(self, name: str) -> None:
        self.name = name
        self._funcs = {}
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"NameSpace {self.name}: {self._funcs}"
    
    def add_function(self, func: MCFunc):
        if not isinstance(func, MCFunc):
            raise TypeError("You can add only functions, decorated with @mc_function")
        func._add_namespace(self)
        self._funcs[func.name] = func


class DataPack:
    def __init__(self, *args: NameSpace, pack_format: int = LATEST_FORMAT, description: str = "") -> None:
        self.spaces = {}
        for i in args:
            self.spaces[i.name] = i
        
        self.pack_format = pack_format
        self.description = description
    
    def add_namespace(self, name: str | NameSpace):
        if isinstance(name, str):
            self.spaces[name] = NameSpace(name)
        elif isinstance(name, NameSpace):
            self.spaces[name.name] = name
        else:
            raise TypeError("Only str and NameSpace objects are acceptable")
    
    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            try:
                return self.spaces[__name]
            except KeyError:
                raise AttributeError("No NameSpace with such name")
    
    def __getitem__(self, index):
        return self.__getattribute__(index)