"""Test generic set."""

# pkg
from attrbox.fn import set_path


def test_empty_path_dict() -> None:
    have = set_path({"a": 1}, [], "ignored")
    want = {"a": 1}
    assert have == want


def test_empty_path_list() -> None:
    have = set_path([1], [], "ignored")
    want = [1]
    assert have == want


def test_simple_update_dict() -> None:
    have = set_path({"a": 1}, "a", 2)
    want = {"a": 2}
    assert have == want


def test_simple_update_list() -> None:
    have = set_path([1], 0, 2)
    want = [2]
    assert have == want


def test_simple_add_dict() -> None:
    have = set_path({"a": 1}, "b", 2)
    want = {"a": 1, "b": 2}
    assert have == want


def test_simple_add_list() -> None:
    have = set_path([1], 2, "extended")
    want = [1, None, "extended"]
    assert have == want


def test_simple_replace_dict() -> None:
    have = set_path({"a": 1}, ["a", 0], 2)
    want = {"a": [2]}
    assert have == want


def test_simple_replace_list() -> None:
    have = set_path([1], [0, "a"], 2)
    want = [{"a": 2}]
    assert have == want


def test_nested_update_dict() -> None:
    have = set_path({"a": [{"b": 1}]}, ["a", 1, "c"], 2)
    want = {"a": [{"b": 1}, {"c": 2}]}
    assert have == want


def test_nested_update_list() -> None:
    have = set_path([{"a": {"b": 1}}], [0, "a", "c"], 2)
    want = [{"a": {"b": 1, "c": 2}}]
    assert have == want


def test_bad_paths_dict() -> None:
    have = set_path({"a": 1}, 0, "works")
    want = {"a": 1, 0: "works"}
    assert have == want


def test_bad_paths_list() -> None:
    have = set_path([1], "a", "works")
    want = [1, {"a": "works"}]
    assert have == want
