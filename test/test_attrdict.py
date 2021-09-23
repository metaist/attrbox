#!/usr/bin/env python
# coding: utf-8
"""Test `AttrDict`."""

# native
from pathlib import Path
import json
import toml

# pkg
from attrbox import AttrDict

HERE = Path(__file__).parent


def test_lshift_json():
    """Expect to load JSON file."""
    # See: https://cloud.google.com/appengine/docs/admin-api/creating-config-files
    path = HERE / "example-appengine.json"
    config = AttrDict() << json.load(path.open())
    value = config.deployment.files["example-resource-file1"].sourceUrl
    expect = "https://storage.googleapis.com/[MY_BUCKET_ID]/example-application/example-resource-file1"
    assert value == expect, "expect to get valid value"


def test_lshift_toml():
    """Expect to load TOML document."""
    # See: https://github.com/toml-lang/toml
    path = HERE / "example-toml.toml"
    config = AttrDict() << toml.load(path.open())
    value = config.servers.alpha.ip
    expect = "10.0.0.1"
    assert value == expect, "expect to get valid value"
