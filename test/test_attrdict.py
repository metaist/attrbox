"""Test `AttrDict`."""

# native
from pathlib import Path
from typing import Any
from typing import Dict
import json

# lib
import tomli as tomllib  # TODO 2026-10-04 [3.10 EOL]: switch to native tomllib

# pkg
from attrbox import AttrDict

HERE = Path(__file__).parent


def test_lshift_json() -> None:
    """Expect to load JSON file."""
    # See: https://cloud.google.com/appengine/docs/admin-api/creating-config-files
    path = HERE / "example-appengine.json"
    config = AttrDict() << json.load(path.open(encoding="utf-8"))

    have = config.get(["handlers", 0, "script", "scriptPath"])
    want = "example-python-app.py"
    assert want == have, "expect to get valid value"


def test_lshift_toml() -> None:
    """Expect to load TOML document."""
    # See: https://github.com/toml-lang/toml
    path = HERE / "example-toml.toml"
    config = AttrDict() << tomllib.loads(path.read_text())

    want = "10.0.0.1"
    have = config.get("servers.alpha.ip".split("."))
    assert want == have, f"expect to get {want}"


def test_merge_empty() -> None:
    """Expect no change."""
    one = AttrDict(a=1, b=2)
    two: Dict[Any, Any] = {}

    want = dict(a=1, b=2)
    have = one << two
    assert want == have, "expect no change"


def test_update() -> None:
    """Expect a basic merges to work."""
    one = AttrDict(a=1, b=2)
    two = dict(a=3)

    want = dict(a=3, b=2)
    have = one << two
    assert want == have, "expect overwrite one value"

    one = AttrDict(a=1, b=2)
    two = dict(a=3, b=4)
    want = dict(a=3, b=4)
    have = one << two
    assert want == have, "expect overwrite both"


def test_extend() -> None:
    """Expect to add new value."""
    one = AttrDict(a=1, b=2)
    two = dict(c=3)

    want = dict(a=1, b=2, c=3)
    have = one << two
    assert want == have, "expect new value"


def test_nested() -> None:
    """Expect basic nesting to merge."""
    one = AttrDict(a=1, b=dict(c=3, d=4))
    two = dict(b=dict(c=5))

    want = dict(a=1, b=dict(c=5, d=4))
    have = one << two
    assert want == have, "expect 1-nested merge"


def test_double_nested() -> None:
    """Expect double nesting to merge."""
    one = AttrDict(a=1, b=dict(c=3, d=dict(e=4, f=5)))
    two = dict(b=dict(d=dict(f=6)))

    want = dict(a=1, b=dict(c=3, d=dict(e=4, f=6)))
    have = one << two
    assert want == have, "expect 2-nested merge"
