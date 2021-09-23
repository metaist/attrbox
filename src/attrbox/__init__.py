#!/usr/bin/env python
# coding: utf-8
"""Attribute-based data structures.

.. include:: ../../README.md
   :start-line: 4
"""

__all__ = (
    "__url__",
    "__version__",
    "__pubdate__",
    "__author__",
    "__email__",
    "__copyright__",
    "__license__",
    "dict_merge",
    "dict_set",
    "dict_get",
    "AttrDict",
    "AttrList",
    "JSend",
)

# pkg
from .__about__ import (
    __url__,
    __version__,
    __pubdate__,
    __author__,
    __email__,
    __copyright__,
    __license__,
)
from .attrdict import AttrDict, dict_merge, dict_set, dict_get
from .attrlist import AttrList
from .jsend import JSend
