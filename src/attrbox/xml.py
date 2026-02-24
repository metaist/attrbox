"""A loader for XML based configuration files.

This is essentially a thin wrapper for
[xmltodict](https://github.com/martinblech/xmltodict). Note that at this time,
streaming XML is not supported.

Requires the [xml] extra to be installed, otherwise a ModuleNotFound error will
be thrown.
"""

# native
import importlib.util
from typing import Any
from typing import Dict

# pkg
from .env import SupportsRead


def parser_available() -> bool:
    """Returns True if the [xml] extra is installed.
    This checks for the existence of the xmltodict package.

    Returns:
        bool: True if the parser is available
    """
    return importlib.util.find_spec("xmltodict") is not None


def _guard_parser_available() -> None:
    """Guard for the parser availability.
    This effectively just throws the appropriate ModuleNotFoundError when parser_available() is not installed.

    Raises:
        ModuleNotFoundError: raised if the [xml] extra is not installed.
    """
    if not parser_available():  # pragma: no cover
        raise ModuleNotFoundError(
            "Please install the [xml] extra to use the XML importer"
        )


def load(file: SupportsRead, /) -> Dict[str, Any]:
    """Load an XML file and translate it to a Dict-like format.

    Args:
        file (SupportsRead): file-like object (has `.read()`)

    Returns:
        Dict[str, Any]: Dict-formatted XML document.

    Raises:
        ModuleNotFoundError: raised if the [xml] extra is not installed.

    Examples:
        >>> from pathlib import Path
        >>> root = Path(__file__).parent.parent.parent
        >>> load((root / "test/config_4.xml").open())
        {'section': {'key': 'value4', 'xml': 'loaded'}}
    """
    _guard_parser_available()
    return loads(file.read())


def loads(text: str, /) -> Dict[str, Any]:
    """Parse an XML string and translate it to a Dict-like format.

    Args:
        text (str): text to parse.

    Returns:
        Dict[str, Any]: Dict-formatted XML document.

    Raises:
        ModuleNotFoundError: raised if the [xml] extra is not installed.

    Examples:
        Elements get turned into keys/values:
        >>> xml_str = "<section><key>value</key></section>"
        >>> loads(xml_str)
        {'section': {'key': 'value'}}

        Repeated keys make an array:
        >>> xml_str = "<section><keys>value1</keys><keys>value2</keys></section>"
        >>> loads(xml_str)
        {'section': {'keys': ['value1', 'value2']}}

        Attributes split up an element:
        >>> xml_str = '<el name="value">inner text</el>'
        >>> loads(xml_str)
        {'el': {'@name': 'value', '#text': 'inner text'}}
    """
    _guard_parser_available()

    import xmltodict

    return xmltodict.parse(text)
