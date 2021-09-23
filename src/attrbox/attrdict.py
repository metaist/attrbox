#!/usr/bin/env python
# coding: utf-8
"""Attribute-based dictionary."""

# native
from typing import Any, Dict, Type

ADict = Dict[Any, Any]
"""`Dict` with `Any` key and `Any` value."""


def dict_merge(dest: ADict, *sources: ADict, default: Type[ADict] = dict) -> ADict:
    """Recursively merge dictionaries into the first dictionary.

    Args:
        dest (dict): dict into which source dicts are merged
        *sources (dict): dicts to merge
        default (dict): constructor for default dict, default: `dict`

    Returns:
        dest (dict): the resulting merged dict

    Examples:
        >>> a = {"b": {"c": 1}, "d": 2}
        >>> b = {"b": {"c": 2, "e": 3}, "d": 2}
        >>> c = {"d": 4}
        >>> dict_merge(a, b, c)
        {'b': {'c': 2, 'e': 3}, 'd': 4}
    """
    for src in sources:
        for key, value in src.items():
            if isinstance(value, dict):
                node = dest.setdefault(key, default())
                dict_merge(node, default(**value), default=default)
            else:
                dest[key] = value
    return dest


def dict_set(dest: ADict, path: str, val: Any, sep: str = ".") -> ADict:
    """Set a path in a dict to a value.

    Args:
        dest (dict): dict to update
        path (str): location to update
        val (any): value to set
        sep (str): path separator (default: .)

    Examples:
        >>> items = {"a": {"b": {"c": 1, "d": 2}}}
        >>> dict_set(items, "a.b.c", 5)
        {'a': {'b': {'c': 5, 'd': 2}}}

        >>> dict_set(items, "a.b.d.e", 5)
        {'a': {'b': {'c': 5, 'd': {'e': 5}}}}

        >>> dict_set(items, "", "") == items
        True

        You can use a different path separator:
        >>> dict_set(items, "a/b/d/e", 6, sep="/")
        {'a': {'b': {'c': 5, 'd': {'e': 6}}}}
    """
    if not path:
        return dest
    original = dest
    parts = path.split(sep)
    for part in parts[:-1]:
        if part not in dest or not isinstance(dest[part], dict):
            dest[part] = {}
        dest = dest[part]
    dest[parts[-1]] = val
    return original


def dict_get(src: ADict, path: str, default: Any = None, sep: str = ".") -> Any:
    """Get a path value from a dict.

    Examples:
        >>> items = {"a": {"b": {"c": 1, "d": 2}}}
        >>> dict_get(items, "a.b.c")
        1
        >>> dict_get(items, "x") is None
        True

        >>> dict_get(items, "") == items
        True
    """
    if not path:
        return src

    parts = path.split(sep)
    for part in parts[:-1]:
        src = src.get(part, {})
    return src.get(parts[-1], default)


class AttrDict(Dict[str, Any]):
    """Like a `dict`, but with attribute syntax."""

    def __setattr__(self, name: str, value: Any) -> None:
        """Set the value of an attribute.

        Args:
            name (str): name of the attribute
            value (any): value to set

        Examples:
            >>> item = AttrDict()
            >>> item.a = 1
            >>> item['a']
            1

            >>> object.__setattr__(item, 'b', 2)
            >>> item.b = 3
            >>> item.b
            3
        """
        try:
            super().__getattribute__(name)
            super().__setattr__(name, value)
        except AttributeError:
            self[name] = value

    def __getattr__(self, name: str) -> Any:
        """Return the value of the attribute.

        Args:
            name (str): name of the attribute

        Returns:
            (any): value of the attribute, or None if it is missing

        Examples:
            >>> item = AttrDict(a=1)
            >>> item.a
            1
        """
        return self[name]

    def __delattr__(self, name: str) -> None:
        """Delete the attribute.

        Args:
            name (str): name of the attribute

        Examples:
            >>> item = AttrDict(a=1, b=2)
            >>> del item.a
            >>> item.a is None
            True
        """
        del self[name]

    def __getitem__(self, name: Any) -> Any:
        """Return the value of the key.

        Args:
            name (str): name of the key

        Returns:
            (any): value of the key, or None if it is missing

        Examples:
            >>> item = AttrDict(a=1)
            >>> item['a']
            1
        """
        result = None
        try:
            result = dict.__getitem__(self, name)
        except KeyError:
            pass
        return result

    def __lshift__(self, other: ADict) -> ADict:
        """Merge `other` into this dict.

        NOTE: Any nested dictionaries will be converted to `AttrDict` objects.

        Args:
            other (dict): other dictionary to merge

        Returns:
            self (AttrDict): merged dictionary

        Examples:
            >>> item = AttrDict(a=1, b=2)
            >>> item <<= {"b": 3}
            >>> item.b
            3

            >>> item << {"b": 2, "c": {"d": 4}} << {"c": {"d": 5}}
            {'a': 1, 'b': 2, 'c': {'d': 5}}
            >>> item.c.d
            5
        """
        return dict_merge(self, other, default=self.__class__)
