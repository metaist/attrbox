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

    have = config.get(["deployment", "files", "example-resource-file1", "sourceUrl"])
    want = "https://storage.googleapis.com/[MY_BUCKET_ID]/example-application/example-resource-file1"
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
    a = AttrDict(a=1, b=2)
    b: Dict[Any, Any] = {}

    want = dict(a=1, b=2)
    have = a << b
    assert want == have, "expect no change"


def test_update() -> None:
    """Expect a basic merges to work."""
    a = AttrDict(a=1, b=2)
    b = dict(a=3)

    want = dict(a=3, b=2)
    have = a << b
    assert want == have, "expect overwrite one value"

    a = AttrDict(a=1, b=2)
    b = dict(a=3, b=4)
    want = dict(a=3, b=4)
    have = a << b
    assert want == have, "expect overwrite both"


def test_extend() -> None:
    """Expect to add new value."""
    a = AttrDict(a=1, b=2)
    b = dict(c=3)

    want = dict(a=1, b=2, c=3)
    have = a << b
    assert want == have, "expect new value"


def test_nested() -> None:
    """Expect basic nesting to merge."""
    a = AttrDict(a=1, b=dict(c=3, d=4))
    b = dict(b=dict(c=5))

    want = dict(a=1, b=dict(c=5, d=4))
    have = a << b
    assert want == have, "expect 1-nested merge"


def test_double_nested() -> None:
    """Expect double nesting to merge."""
    a = AttrDict(a=1, b=dict(c=3, d=dict(e=4, f=5)))
    b = dict(b=dict(d=dict(f=6)))

    want = dict(a=1, b=dict(c=3, d=dict(e=4, f=6)))
    have = a << b
    assert want == have, "expect 2-nested merge"
