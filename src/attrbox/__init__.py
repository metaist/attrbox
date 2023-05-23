"""Functional-style and attribute-based data structures.

.. include:: ../../README.md
   :start-line: 4
"""
__version__ = "0.1.1"
__all__ = (
    "__version__",
    "AttrDict",
    "AttrList",
    "Fn",
    "JSend",
)

# pkg
from .attrdict import AttrDict
from .attrlist import AttrList
from .fn import Fn

from .jsend import JSend
