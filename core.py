from typing import Any, Callable

LATEST_FORMAT = 15


class NameSpace:
    def __init__(self, name: str) -> None:
        self.name = name
        self._funcs = {}
    
    def add_function(self, func: Callable, name: str = None):
        if not hasattr(func, "__mc__"):
            raise TypeError("You can add only functions, decorated with @mc_function")
        name = name if name is not None else func.__name__
        self._funcs[name] = func


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