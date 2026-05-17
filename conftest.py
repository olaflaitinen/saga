"""Root-level pytest configuration.

Registers custom markers for unit, integration, and property tests so that
each test class can be invoked selectively (e.g., `pytest -m unit`).
"""

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers", "unit: mark a test as a unit test (no I/O, no model training)."
    )
    config.addinivalue_line(
        "markers", "integration: mark a test as an integration test (may instantiate models)."
    )
    config.addinivalue_line(
        "markers", "property: mark a test as a property-based test using Hypothesis."
    )
    config.addinivalue_line(
        "markers", "slow: mark a test as slow (skipped in fast CI runs)."
    )
