#! python3

import doctest
import functools
import operator as op

import hypothesis.strategies as st

from result import Result


def test_docs():
    """Broken examples in documentation are terrible."""
    doctest.testfile('README.rst')


@st.composite
def test_integer_maths(draw):
    """Simple maths with integers is fast and it's easy to make the functions,
    but Hypothesis makes the test surprisingly powerful.
    """
    # Construct a list of unary functions on integers
    ops = st.sampled_from([op.add, op.sub, op.floordiv, op.mul, op.pow])
    funcs = [functools.partial(draw(ops), draw(st.integers()))
             for _ in range(draw(st.integers(1, 10)))]
    # Draw an initial value, and calculate the output as Result
    initial = draw(st.integers())
    res = Result(initial)
    for func in funcs:
        res = res.then(func)
    # Assert that the results were identical, or the same exception was thrown
    try:
        for func in funcs:
            initial = func(initial)
        assert initial == res.ok
    except Exception as err:
        assert type(err) == type(res.err)


def test_result_flattens():
    assert Result(1) == Result(Result(Result(1)))
