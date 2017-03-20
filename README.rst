Monadic Control in Python
=========================

This is an experimental module for playing with the result monad in Python,
which interfaces fairly nicely with exceptions.

As well as checking the ``res.ok`` and ``res.err`` values, you can
``res.unwrap()`` - which raises the ``err`` exception or returns the
``ok`` value.  It's also safe to use ``Result.unwrap`` on any other value -
it will be returned unchanged.

You can apply a series of functions with ``res.then(func1).then(func2)``.
You can even decorate your own functions with ``@Result.decorate`` to
transform any return value or thrown exception into a result value.

Here's some examples::

    >>> from result import Result
        Result(1).then(lambda x: x + 1).then(lambda x: x ** 2)
    Result(ok=4)

    >>> Result([1, 2, 3]).then(lambda x: x[4])
    Result(err=list index out of range)

    >>> Result(1).unwrap() == Result.unwrap(1) == 1
    True

    >>> @Result.decorate
        def my_func(x):
            return 1 / x

        my_func(2)
    Result(ok=0.5)

    >>> my_func(0)
    Result(err=division by zero)

Comments on ergonomics or edge cases welcome.
