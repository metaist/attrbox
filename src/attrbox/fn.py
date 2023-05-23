#!/usr/bin/env python
# coding: utf-8
"""Convert `dict` and `list` into functional objects."""

# native
from __future__ import annotations
from copy import copy
from typing import Any
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Optional
from typing import TypeVar
from typing import Union

# pkg
from .attrdict import AttrDict
from .attrlist import AttrList


Self = TypeVar("Self", bound="Fn")
"""An instance of `Fn`."""

Wrappable = Union[List[Any], Mapping[str, Any]]
"""Type of objects that can be wrapped."""


def wrap_list(item: Iterable[Any]) -> AttrList:
    """Return an iterable wrapped in an `AttrList`."""
    return AttrList([Fn.wrap(v) for v in item])


def wrap_dict(item: Mapping[str, Any]) -> AttrDict:
    """Return a mapping wrapped in an `AttrDict`."""
    return AttrDict({k: Fn.wrap(v) for k, v in item.items()})


class Fn:
    """Functional wrapper for a `List` or `Mapping`."""

    _item: Wrappable
    """The wrapped item."""

    # constructors #

    def __init__(self, item: Union[Fn, Wrappable]):
        """Construct a new functional wrapper.

        >>> Fn(Fn([1, 2, 3])) == [1, 2, 3]
        True
        >>> Fn(5)
        Traceback (most recent call last):
             ...
        ValueError: Cannot wrap this type: <class 'int'>
        """
        if isinstance(item, Fn):
            self._item = item._item
        elif isinstance(item, List):
            self._item = wrap_list(item)
        elif isinstance(item, Mapping):
            self._item = wrap_dict(item)
        else:
            raise ValueError(f"Cannot wrap this type: {type(item)}")

    def copy(self) -> Fn:
        """Return a shallow copy.

        >>> items = Fn([1, 2, 3])
        >>> copy = items.copy()
        >>> copy is not items
        True
        >>> copy == items
        True
        """
        return self.__class__(copy(self._item))

    @classmethod
    def wrap(cls, item: Wrappable) -> Union[Fn, Any]:
        """Recursively replace `dict` and `list` with functional equivalents.

        Args:
            item (Any): typically a `dict` or `list`

        Returns:
            Any: `item` or a wrapped version of `item`

        Examples:

            Wrapping simple values returns those values:
            >>> items = Fn.wrap([{"a": [1, {"b": 2}, 3]}, {"a": [4, {"b": 5}, 6]}])
            >>> isinstance(items, Fn)
            True

            Wrapping multiple times has no impact:
            >>> items = Fn.wrap([1, 2, 3])
            >>> Fn.wrap(items) is items
            True
        """
        result: Union[Fn, Any] = item
        if isinstance(item, Fn):
            pass
        elif isinstance(item, List):
            result = Fn(wrap_list(item))
        elif isinstance(item, Mapping):
            result = Fn(wrap_dict(item))
        return result

    @classmethod
    def fromkeys(cls, iterable: Iterable[str], value: Optional[Any] = None, /) -> Fn:
        """Create a new dictionary with keys from iterable and values set to value.

        Args:
            iterable (Iterable[str]): iterable of strings that will be used for keys
            value (Any, optional): value for each new key. Defaults to `None`.

        Returns:
            Fn: new wrapped dict

        Examples:
            >>> items = Fn.fromkeys("abc")
            >>> isinstance(items, Fn)
            True
            >>> items == {"a": None, "b": None, "c": None}
            True
        """
        return cls({k: value for k in iterable})

