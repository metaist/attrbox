"""Attribute-based data structures.

.. include:: ../../README.md
   :start-line: 4
"""

# pkg
from .attrdict import AttrDict, __pdoc__ as doc1
from .attrlist import AttrList, __pdoc__ as doc2

from .jsend import JSend

__version__ = "0.1.1"
__all__ = (
    "__version__",
    "AttrDict",
    "AttrList",
    "JSend",
)

# Update pdoc at all levels.
__pdoc__ = {}
for doc in [doc1, doc2]:
    __pdoc__.update(doc)
