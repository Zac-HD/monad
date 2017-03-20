#! python3

import doctest
import functools
import operator as op

import hypothesis.strategies as st
from hypothesis import given

from result import Result


def test_docs():
    """Broken examples in documentation are terrible."""
    doctest.testfile('README.rst')


integer_funcs = st.tuples(
    st.sampled_from([op.add, op.sub, op.floordiv, op.mul]),
    st.integers()
    ).map(lambda v: functools.partial(v[0], v[1]))

@given(initial=st.integers(), funcs=st.lists(integer_funcs))
def test_integer_maths(initial, funcs):
    """Simple maths with integers is fast and it's easy to make the functions,
    but Hypothesis makes the test surprisingly powerful.
    """
    res = Result(initial)
    for func in funcs:
        res = res.then(func)
    try:
        for func in funcs:
            initial = func(initial)
        assert initial == res.ok
    except Exception as err:
        assert type(err) == type(res.err)


def test_result_flattens():
    assert Result(1) == Result(Result(Result(1)))
