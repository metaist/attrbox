"""Generic container-based algorithms."""

# native
from __future__ import annotations
from typing import Any
from typing import Mapping
from typing import Type
from typing import Dict

GenericDict = Dict[Any, Any]
"""Generic `dict`"""


def dict_merge(
    dest: GenericDict,
    *sources: Mapping[Any, Any],  # read-only
    default: Type[GenericDict] = dict,
) -> GenericDict:
    """Generic recursive merge for dict-like objects.

    NOTE: Every nested `dict` will pass through `default`.

    Args:
        dest (GenericDict): dict into which `sources` are merged
        *sources (Mapping[Any, Any]): dicts to merge
        default (Type[GenericDict], optional): constructor for default `dict`.
            Defaults to `dict`.

    Returns:
        SupportsItem: the resulting merged dict

    Examples:
        >>> a = {"b": {"c": 1}, "d": 2}
        >>> b = {"b": {"c": 2, "e": 3}, "d": 2}
        >>> c = {"d": {"e": 5}}
        >>> dict_merge(a, b, c)
        {'b': {'c': 2, 'e': 3}, 'd': {'e': 5}}
    """
    for src in sources:
        for key, value in src.items():
            if not isinstance(value, Mapping):
                # overwrite with simple value
                dest[key] = value
                continue

            value = default(value)
            prev = dest.get(key, {})
            if isinstance(prev, dict):  # extendable
                if not isinstance(prev, default):
                    prev = default(prev)
                dest[key] = dict_merge(prev, value, default=default)
            else:  # cannot extend
                dest[key] = value
    return dest
