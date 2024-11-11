from functools import wraps
from inspect import iscoroutinefunction

from asgiref.sync import async_to_sync


def ensure_sync(func):
    """
    Add this decorator to async views, before adding decorators
    from other extensions (like flask_smorest) which don't support
    async views.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if iscoroutinefunction(func):
            return async_to_sync(func)(*args, **kwargs)

        return func(*args, **kwargs)

    return wrapper
