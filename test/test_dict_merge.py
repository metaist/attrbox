#!/usr/bin/env python
# coding: utf-8
"""Test `dict_merge` functions."""

from attrbox import dict_merge


def test_merge_empty():
    """Expect no change."""
    a = dict(a=1, b=2)
    b = {}
    expect = dict(a=1, b=2)
    assert dict_merge(a, b) == expect, "expect no change"


def test_update():
    """Expect a basic merges to work."""
    a = dict(a=1, b=2)
    b = dict(a=3)
    expect = dict(a=3, b=2)
    assert dict_merge(a, b) == expect, "expect overwrite one value"

    a = dict(a=1, b=2)
    b = dict(a=3, b=4)
    expect = dict(a=3, b=4)
    assert dict_merge(a, b) == expect, "expect overwrite both"


def test_extend():
    """Expect to add new value."""
    a = dict(a=1, b=2)
    b = dict(c=3)
    expect = dict(a=1, b=2, c=3)
    assert dict_merge(a, b) == expect, "expect new value"


def test_nested():
    """Expect basic nesting to merge."""
    a = dict(a=1, b=dict(c=3, d=4))
    b = dict(b=dict(c=5))
    expect = dict(a=1, b=dict(c=5, d=4))
    assert dict_merge(a, b) == expect, "expect 1-nested merge"

    a = dict(a=1, b=dict(c=3, d=dict(e=4, f=5)))
    b = dict(b=dict(d=dict(f=6)))
    expect = dict(a=1, b=dict(c=3, d=dict(e=4, f=6)))
    assert dict_merge(a, b) == expect, "expect 2-nested merge"
