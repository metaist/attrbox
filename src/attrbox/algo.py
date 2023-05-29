"""Generic container-based algorithms."""

# native
from __future__ import annotations
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Mapping
from typing import Optional
from typing import Protocol
from typing import runtime_checkable
from typing import SupportsIndex
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union
from typing import Tuple
from typing import Dict

if TYPE_CHECKING:  # pragma: no cover
    from _typeshed import SupportsRichComparison
else:
    SupportsRichComparison = Any

T = TypeVar("T")
"""A generic type."""

FilterFn = Callable[[Any, Any], bool]
"""`.filter` signature `(key, value) => included?`"""

EachFn = Callable[[Any, Any], None]
"""`.each` signature `(key, value) => None`"""

GroupFn = Callable[[Any, Any], Any]
"""`.group` signature `(key, value) => new_key`"""

MapFn = Callable[[Any, Any], Any]
"""`.map` signature `(key, value) => new_value`"""

ReduceFn = Callable[[T, Any, Any], T]
"""`.reduce` signature `(result, key, value) => new_result`"""

SortFn = Callable[[Any], SupportsRichComparison]
"""`.sort` signature `(value) => sortable_value`"""

SingleItemKey = Union[str, SupportsIndex, slice]
"""Basic index into an object that `SupportsItem`"""

ItemKey = Union[SingleItemKey, Iterable[SingleItemKey]]
"""Basic and path-like index into an object that `SupportsItem`"""

GenericDict = Dict[Any, Any]
"""Generic `dict`"""


@runtime_checkable
class SupportsItem(Protocol):  # pragma: no cover
    """Protocol for Mapping-like objects.

    Requires:
        - `k in d`
        - `d[k]`
        - `d[k] = v`
        - `d.get(k)`
        - `d.items()
    """

    def __contains__(self, key: Any, /) -> Any:
        """Typically returns `True` if `key` exists, `False` otherwise."""

    def __getitem__(self, key: ItemKey) -> Any:
        """Return value of `key`."""

    def __setitem__(self, key: ItemKey, value: Any) -> Optional[Any]:
        """Set `key` to `value`."""

    def get(self, key: ItemKey, /, default: Optional[Any]) -> Any:
        """Return value associated with `key` or `default` if not found."""

    def items(self) -> Iterable[Tuple[ItemKey, Any]]:
        """Return keys and values."""


def nop(*_: Any) -> None:
    """Always return `None`."""
    return None


def identity(v: T) -> T:
    """Return the argument."""
    return v


def firstarg(v: T, *_: Any) -> T:
    """Return first argument."""
    return v


def lastarg(*_: Any, v: T) -> T:
    """Return last argument."""
    return v


def truthy(*_: Any, v: Any) -> bool:
    """Return `True` if last argument is truthy."""
    return bool(v[-1])


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


def dict_get(items: GenericDict, key: ItemKey, default: Optional[Any] = None, /) -> Any:
    if isinstance(key, str):
        return dict.get(items, key, default)
    if isinstance(key, slice):
        return items[key]

    src: SupportsItem = items
    result: Any = default
    try:
        for step in key:
            result = src[step]  # take step
            if isinstance(result, SupportsItem):
                src = result  # preserve context
    except (KeyError, IndexError, TypeError):
        # key doesn't exist, index is unreachable, or item is not indexable
        result = default
    return result
