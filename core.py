from __future__ import annotations
from typing import Any, Callable
from commands.decorators import command
from structures.text import Text
import commands.decorators
import os
import json

LATEST_FORMAT = 18
func_tag = {
    "load": [],
    "tick": []
}


class NameSpace:
    def __init__(self, name: str) -> None:
        self.name = name
        self._funcs: list[MCFunc] = []
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"NameSpace {self.name}: {self._funcs}"
    
    def add_function(self, func: MCFunc):
        if not isinstance(func, MCFunc):
            raise TypeError("You can add only functions, decorated with @mc_function")
        func.set_namespace(self)
        self._funcs.append(func)
    
    def _gen_funcs(self, path: str):
        os.makedirs(os.path.join(path, self.name, "functions"), exist_ok=True)
        
        for f in self._funcs:
            global func_tag
            if hasattr(f, "_load"):
                func_tag["load"].append(f)
            if hasattr(f, "_tick"):
                func_tag["tick"].append(f)
            with open(os.path.join(path, self.name, "functions", f.path), 'w') as file:
                file.write(f.gen_func())


default_namespace = NameSpace("pydp")

class MCFunc:
    gen_func: Callable
    namespace: NameSpace
    name: str
    path: str
    
    def __init__(self, gen_func: Callable, name: str = None, path: str = "") -> None:
        self.gen_func = gen_func
        self.namespace = None
        self.name = name if name is not None else gen_func.__name__
        self.path = f"{path}/{name}.mcfunction" if path else f"{name}.mcfunction"
    
    @command
    def __call__(self) -> Any:
        if self.namespace:
            return f"function {self.namespace}:{self.name}"
        raise RuntimeError("You can't call mc_function without namespace defined")
    
    def __str__(self) -> str:
        if self.namespace:
            return f"{self.namespace}:{self.name}"
        raise RuntimeError("No namespace specified for this function")
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def set_namespace(self, namespace: NameSpace):
        self.namespace = namespace
    

def mc_function(func: Callable = None, /, *, namespace: NameSpace = None, func_name: str = None, log: bool = False, path: str = ""):
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
        nonlocal func_name, namespace, log, path
        
        def gen_func(*args, **kwargs):
            func(*args, **kwargs)
            out = "\n".join(commands.decorators.fun_buf)
            commands.decorators.fun_buf.clear()
            return out

        if log:
            print(f"{func_name if func_name else func.__name__}:\n\t{"\n\t".join(gen_func().splitlines())}")
        
        mc_func = MCFunc(gen_func, func_name if func_name else func.__name__, path)
        
        if namespace:
            namespace.add_function(mc_func)
        else:
            default_namespace.add_function(mc_func)
        
        return mc_func

    if not func:
        return inner
    return inner(func)


def tick(func: MCFunc):
    """Decorator to define `@mc_function` to be tick function. Tick function is a function which works every game tick."""
    func._tick = True
    return func


def load(func: MCFunc):
    """Decorator to define `@mc_function` to be load function. Load function is a function which works on datapack load."""
    func._load = True
    return func


class DataPack:
    def __init__(self, *args: NameSpace, pack_name: str = "PyDatapack", datapack_path: str = "", pack_format: int = LATEST_FORMAT, description: str | Text = "") -> None:
        self.spaces: list[NameSpace] = []
        for i in args:
            self.spaces.append(i)
        
        self.spaces.append(default_namespace)
        self.pack_format = pack_format
        self.description = description
        self.pack_name = pack_name
        self.datapack_path = datapack_path
    
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
    
    def generate(self):
        os.makedirs(os.path.join(self.datapack_path, self.pack_name, "data"), exist_ok=True)
        
        # Generating pack.mcmeta
        with open(os.path.join(self.datapack_path, self.pack_name, "pack.mcmeta"), "w") as file:
            json.dump(
                {
                    "pack": {
                        "description": str(self.description),
                        "pack_format": self.pack_format
                    }
                },
                file
            )
        
        # Generating all namespaces
        for n in self.spaces:
            n._gen_funcs(os.path.join(self.datapack_path, self.pack_name, "data"))
        
        # Generating tag for tick and load functions
        global func_tag
        tag_path = os.path.join(self.datapack_path, self.pack_name, "data", "minecraft", "tags", "functions")
        os.makedirs(tag_path, exist_ok=True)
        
        with open(os.path.join(tag_path, "load.json"), 'w') as file:
            json.dump(
                {
                    "values": list(map(str, func_tag["load"]))
                },
                file
            )
        
        with open(os.path.join(tag_path, "tick.json"), 'w') as file:
            json.dump(
                {
                    "values": list(map(str, func_tag["tick"]))
                },
                file
            ) 
        