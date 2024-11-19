import dataclasses
from inspect import iscoroutinefunction, ismethod
from typing import Any, Callable


@dataclasses.dataclass
class Call:
    name: str
    args: tuple = ()
    kwargs: dict[str, Any] = dataclasses.field(default_factory=dict)


class Spy:
    """
    Spy all method calls on the given object.

    The method calls will be available is the method_calls field, which is a list of Call.
    """

    def __init__(self, obj) -> None:
        self.method_calls: list[Call] = []
        self._spy_all_methods(obj)

    def _spy_all_methods(self, obj):
        method_names = [attr for attr in dir(obj) if ismethod(getattr(obj, attr))]

        for method_name in method_names:
            method = getattr(obj, method_name)
            if iscoroutinefunction(method):
                self._spy_async_method(obj, method)
            else:
                self._spy_sync_method(obj, method)

    def _spy_sync_method(self, obj, func: Callable):
        def wrapper(*args, **kwargs):
            self.method_calls.append(Call(func.__name__, args=args, kwargs=kwargs))
            return func(*args, **kwargs)

        setattr(obj, func.__name__, wrapper)

    def _spy_async_method(self, obj, func: Callable):
        async def wrapper(*args, **kwargs):
            self.method_calls.append(Call(func.__name__, args=args, kwargs=kwargs))
            return await func(*args, **kwargs)

        setattr(obj, func.__name__, wrapper)
