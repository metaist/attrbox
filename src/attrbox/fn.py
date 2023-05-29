#!/usr/bin/env python
# coding: utf-8
"""Convert `dict` and `list` into functional objects."""

# native
from __future__ import annotations
from copy import copy
from typing import Any
from typing import cast
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Mapping
from typing import Optional
from typing import TypeVar
from typing import Union
from operator import attrgetter


# pkg
from .attrdict import AttrDict

# from .attrdict import AttrDictKey
from .attrlist import AttrList
from .algo import firstarg


Self = TypeVar("Self", bound="Fn")
"""`Fn` instance"""

RawDict = Mapping[str, Any]
"""Mapping that will be wrapped."""

RawList = Iterable[Any]
"""Iterable that will be wrapped."""

CanWrap = Union["Fn", RawDict, RawList]
"""Objects that can be wrapped."""

WrappedDict = Mapping[str, Any]
"""Mapping that is wrapped."""

WrappedList = List[Any]
"""List that is wrapped."""

Wrapped = Union[WrappedList, WrappedDict]
"""Wrapped object."""


class Fn:
    """Functional wrapper for a `List` or `Mapping`."""

    _item: Wrapped
    """Wrapped item."""

    _is_dict: bool = False
    """Whether the wrapped item is a `Mapping`."""

    def _asdict(self) -> WrappedDict:
        """Coerce type-checker to treat wrapped item as a `Mapping`."""
        return cast(WrappedDict, self._item)

    def _aslist(self) -> WrappedList:
        """Coerce type-checker to treat wrapped item as a `List`."""
        return cast(WrappedList, self._item)

    # constructors #

    def __init__(self, item: CanWrap):
        """Construct a new functional wrapper.

        >>> Fn(Fn([1, 2, 3])) == [1, 2, 3]
        True

        >>> Fn(5)
        Traceback (most recent call last):
             ...
        ValueError: Cannot wrap this type: <class 'int'>
        """
        cls = self.__class__
        if isinstance(item, cls):
            self._item = item._item  # rewrap
        elif isinstance(item, Mapping):
            self._item = cls._wrap_dict(item)
            self._is_dict = True
        elif isinstance(item, Iterable) and not isinstance(item, str):
            self._item = cls._wrap_list(item)
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
    def _wrap_dict(cls, item: RawDict) -> AttrDict:
        """Return a mapping wrapped in an `AttrDict`."""
        return AttrDict({k: cls.wrap(v) for k, v in item.items()})

    @classmethod
    def _wrap_list(cls, item: RawList) -> AttrList:
        """Return an iterable wrapped in an `AttrList`."""
        return AttrList([cls.wrap(v) for v in item])

    @classmethod
    def wrap(cls, item: CanWrap) -> Union[Fn, Any]:
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

            >>> Fn.wrap(["a", "b", "c"])
            Fn(['a', 'b', 'c'])

            Wrapping multiple times has no impact:
            >>> items = Fn.wrap([1, 2, 3])
            >>> Fn.wrap(items) is items
            True
        """
        result: Union[Fn, Any] = item
        if isinstance(item, Fn):
            pass
        elif isinstance(item, Mapping):
            result = Fn(cls._wrap_dict(item))
        elif isinstance(item, Iterable) and not isinstance(item, str):
            result = Fn(cls._wrap_list(item))
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
            >>> items
            Fn({'a': None, 'b': None, 'c': None})
        """
        return cls({k: value for k in iterable})

    # contents #

    def __getattr__(self, name: str) -> Any:
        """Return missing attributes from the wrapped item."""
        return getattr(self._item, name)

    def __repr__(self) -> str:
        """Return `repr` of the wrapped item.

        >>> repr(Fn([1, 2, 3]))
        'Fn([1, 2, 3])'
        """
        return f"{self.__class__.__name__}({repr(self._item)})"

    def __len__(self) -> int:
        """Return length of the wrapped item.

        >>> len(Fn([1, 2, 3]))
        3
        """
        return len(self._item)

    def __contains__(self, item: Any) -> Any:
        """Return `True` if `item` is in the wrapped object.

        >>> 2 in Fn([1, 2, 3])
        True
        >>> 'a' in Fn({'a': 5})
        True
        """
        return self._item.__contains__(item)

    def __iter__(self) -> Iterator[Any]:
        """Return wrapped item's iterator.

        >>> [x for x in Fn([1, 2, 3])] == [1, 2, 3]
        True
        >>> [x for x in Fn({"a": 1, "b": 2})] == ["a", "b"]
        True
        """
        return iter(self._item)

    def __eq__(self, other: Any) -> Any:
        """Return `True` if `other` has the same contents.

        Args:
            other (Any): other item to compare

        Returns:
            Any: `True` if it has the same contents

        Examples:
            >>> items = Fn([1, 2, 3])
            >>> items == [1, 2, 3]
            True

            >>> other = Fn([1, 2, 3])
            >>> items is other
            False
            >>> items == other
            True
        """
        if isinstance(other, self.__class__):
            return self._item == other._item
        else:
            return self._item == other

    def keys(self) -> Fn:
        """Return the keys/indices.

        >>> Fn([1, 2, 3]).keys()
        Fn([0, 1, 2])
        >>> Fn({"a": 1, "b": 2}).keys()
        Fn(['a', 'b'])
        """
        cls = self.__class__
        if self._is_dict:
            return cls(self._asdict().keys())
        return cls(range(len(self._item)))

    def values(self) -> Fn:
        """Return the values.

        >>> Fn([1, 2, 3]).values()
        Fn([1, 2, 3])
        >>> Fn({"a": 1, "b": 2}).values()
        Fn([1, 2])
        """
        cls = self.__class__
        if self._is_dict:
            return cls(self._asdict().values())
        return self.copy()

    def items(self) -> Fn:
        """Return the key/value pairs.

        >>> Fn([1, 2, 3]).items()
        Fn([Fn([0, 1]), Fn([1, 2]), Fn([2, 3])])
        >>> Fn({"a": 1, "b": 2}).items()
        Fn([Fn(['a', 1]), Fn(['b', 2])])
        """
        cls = self.__class__
        if self._is_dict:
            return cls(self._asdict().items())
        return cls(zip(self.keys(), self.values()))

    def count(self, value: Any, /) -> int:
        """Return the number of occurrences of `value` in the values.

        Args:
            value (any): value to count

        Returns:
            int: number of times value appears

        Examples:
            >>> items = Fn([1, 2, 2])
            >>> items.count(2)
            2
            >>> items.count(5)
            0

            >>> items = Fn(dict(a=1, b=2, c=2))
            >>> items.count(2)
            2
            >>> items.count(5)
            0
        """
        if self._is_dict:
            return list(self._asdict().values()).count(value)
        return self._aslist().count(value)

    def attr(self, *attrs: str) -> Fn:
        """Return attributes from `.values`.

        >>> Fn([{'a': 1}, {'a': 2}]).attr('a')
        Fn([1, 2])
        """
        fn = attrgetter(*attrs) if attrs else firstarg
        assert callable(fn)
        return self.__class__([fn(v) for v in self.values()])

    # def get(self, name: AttrDictKey, default: Optional[Any] = None, /)
    # -> Optional[Any]:
    #     """_summary_

    #     Args:
    #         name (AttrDictKey): _description_
    #         default (Optional[Any], optional): _description_. Defaults to None.

    #     Returns:
    #         Optional[Any]: _description_

    #     Examples:
    #         Normal `.get` functions work:
    #         >>> items = Fn(a=dict(b=[{"c": 3}, {"c": -10}]), d=4)
    #         >>> items.get('d') == 4
    #         True
    #         >>> items.get('e') is None
    #         True
    #         >>> items.get('e', 5) == 5
    #         True

    #         But you can also indexing into nested `list` and `dict`:
    #         >>> items.get(['a', 'b', 1, 'c']) == -10
    #         True

    #         Bad indexing will just return the default:
    #         >>> items.get(['e']) is None # key doesn't exist
    #         True
    #         >>> items.get(['a', 'b', 5]) is None  # index unreachable
    #         True
    #         >>> items.get(['d', 'e']) is None # int is not indexable
    #         True
    #     """
    #     return AttrDict.get(self, name, default)
