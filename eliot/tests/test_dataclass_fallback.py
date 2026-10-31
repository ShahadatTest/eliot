"""Exercise the PyPy JSON fallback without requiring a PyPy interpreter."""

from dataclasses import InitVar, dataclass
import importlib.util
import json
import platform
from typing import ClassVar

import pytest

import eliot.json


@pytest.fixture
def fallback(monkeypatch):
    monkeypatch.setattr(platform, "python_implementation", lambda: "PyPy")
    spec = importlib.util.spec_from_file_location(
        "eliot._test_json_fallback", eliot.json.__file__
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.json_default


def test_dataclass_initvar(fallback):
    @dataclass
    class Example:
        value: int
        transient: InitVar[int]

    value = Example(1, 2)
    assert json.loads(json.dumps(value, default=fallback)) == {"value": 1}


def test_dataclass_classvar(fallback):
    @dataclass
    class Example:
        value: int
        shared: ClassVar[str] = "class configuration"

    assert fallback(Example(1)) == {"value": 1}


def test_dataclass_type_uses_fallback(fallback):
    @dataclass
    class Example:
        value: int

    assert fallback(Example) == repr(Example)


def test_dataclass_regular_fields(fallback):
    @dataclass
    class Example:
        value: int
        label: str = "default"

    assert fallback(Example(1)) == {"value": 1, "label": "default"}
