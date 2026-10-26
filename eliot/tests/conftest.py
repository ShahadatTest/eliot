"""Isolation for tests that use Eliot's process-global destinations."""

import pytest

from eliot._output import BufferingDestination, Logger


@pytest.fixture(autouse=True)
def isolated_destinations(monkeypatch):
    # Keep the Destinations object: the public add/remove APIs are bound to it.
    # Reset its state so adding a destination cannot replay another test's logs.
    destinations = Logger._destinations
    monkeypatch.setattr(destinations, "_destinations", [BufferingDestination()])
    monkeypatch.setattr(destinations, "_any_added", False)
    monkeypatch.setattr(destinations, "_globalFields", {})
