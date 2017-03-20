#! python3
"""An experiment with the Result Monad and exceptions."""

import functools


class Result:
    """Convert control flow from exceptions to the Result monad."""

    def __init__(self, ok=None, err=None):
        """Initialise Result with private ``ok`` and ``err`` values."""
        while isinstance(ok, self.__class__) and err is None:
            ok, err = ok.ok, ok.err
        if err is not None:
            if not isinstance(err, Exception) and not (
                    isinstance(err, type) and isinstance(err(), Exception)):
                raise ValueError('`err` must be an exception or None')
            ok = object()
        self.__ok = ok
        self.__err = err

    @property
    def ok(self):
        return self.__ok

    @property
    def err(self):
        return self.__err

    def unwrap(self):
        """Unwrap the result, returning ``ok`` or raising ``err``.
        Identity function for non-Result values (ie ``unwrap(a) == a``).
        """
        if not isinstance(self, Result):
            return self
        if self.err is not None:
            raise self.err
        return self.ok

    @classmethod
    def decorate(cls, func):
        """A decorator to make any function return a Result.
        Returned values are ``ok``; raised exceptions are ``err``.
        """
        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                args = [cls.unwrap(a) for a in args]
                kwargs = {k: cls.unwrap(v) for k, v in kwargs.items()}
                return cls(ok=func(*args, **kwargs))
            except Exception as err:
                return cls(err=err)
        return inner

    def then(self, func):
        """Easily chain functions with ``result.then(func1).then(func2)``."""
        return self.decorate(func)(self)

    def __repr__(self):
        name = self.__class__.__name__
        if self.err is None:
            return '{}(ok={})'.format(name, self.ok)
        return '{}(err={})'.format(name, self.err)

    def __hash__(self):
        return hash((self.ok, self.err))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self.err is None and other.err is None:
            return self.ok == other.ok
        return self is other
