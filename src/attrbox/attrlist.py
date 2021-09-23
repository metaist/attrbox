#!/usr/bin/env python
# coding: utf-8
"""Attribute-based list."""

# native
from typing import Any, Callable, List, Union
from operator import attrgetter


class AttrList(List[Any]):
    """Like a `list`, but with easy-to-query attributes of members."""

    def __getattr__(self, name: str) -> List[Any]:
        """Return a list of the this attribute in the contained members.


        Examples:
            >>> from . import AttrDict
            >>> items = AttrList([AttrDict(a=1), AttrDict(a=2), AttrDict(a=3, b=4)])
            >>> items.a
            [1, 2, 3]
            >>> items.b
            [None, None, 4]
        """
        return self.attr(name, first=False, unique=False)

    def attr(
        self, attrs: Union[str, List[str]], first: bool = False, unique: bool = False
    ) -> Union[Any, List[Any]]:
        """Return the attribute value of the contained members.

        Args:
            attrs (list[str]): attributes to extract
            first (bool): get first value or None if there are none (default: False)
            unique (bool): only return unique values (default: False)

        Returns:
            (Any or list[Any]): the values of the attribute

        Examples:
            >>> from . import AttrDict
            >>> items = AttrList([AttrDict(a=1), AttrDict(a=2), AttrDict(a=1, b=4)])
            >>> items.attr(["a", "b"])
            [(1, None), (2, None), (1, 4)]

            >>> items.attr("a", first=True)
            1

            >>> items.attr("a", unique=True)
            [1, 2]
        """
        if isinstance(attrs, str):
            attrs = [attrs]

        key = attrgetter(*attrs)
        if first:  # short-circuit
            return key(self[0]) if self else None

        result = [key(member) for member in self]
        if unique:
            result = list(dict.fromkeys(result))
        return result

    def find(self, predicate: Callable[[Any], bool]) -> "AttrList":
        """Return a new AttrList of atom where `predicate` returns `True`.

        Examples:
            >>> from . import AttrDict
            >>> items = AttrList([AttrDict(a=1), AttrDict(a=2), AttrDict(a=3, b=4)])
            >>> isodd = lambda m: m.a % 2 == 1
            >>> items.find(isodd).a
            [1, 3]
        """
        cls = self.__class__
        return cls([member for member in self if predicate(member)])
