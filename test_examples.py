"""
pytest — the standard Python testing framework.

Why SREs care: automation and tooling need tests too. Interviewers love seeing
that you write tests for your scripts. pytest is the de-facto standard: plain
`assert`, fixtures for setup/teardown, and parametrization for many cases.

Install once:  pip install pytest
Run:           pytest test_examples.py -v
               (pytest auto-discovers files named test_*.py and functions test_*)
"""

import pytest


# --- Small "production" functions we want to test --------------------------
def is_prime(n: int) -> bool:
    """Return True if n is a prime number."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def parse_cpu(millicores: str) -> float:
    """Convert a Kubernetes CPU string like '250m' or '2' to a float of cores."""
    if millicores.endswith("m"):
        return int(millicores[:-1]) / 1000
    return float(millicores)


# --- Basic tests: a test is any test_* function that asserts ---------------
def test_is_prime_true():
    assert is_prime(7) is True


def test_is_prime_false():
    assert is_prime(8) is False


# --- Parametrize: run the SAME test with MANY inputs (no copy-paste) --------
@pytest.mark.parametrize(
    "value,expected",
    [
        (2, True),
        (3, True),
        (4, False),
        (1, False),
        (0, False),
        (-5, False),
        (13, True),
    ],
)
def test_is_prime_many(value, expected):
    assert is_prime(value) == expected


@pytest.mark.parametrize(
    "raw,cores",
    [
        ("250m", 0.25),
        ("1000m", 1.0),
        ("2", 2.0),
    ],
)
def test_parse_cpu(raw, cores):
    assert parse_cpu(raw) == cores


# --- Fixture: reusable setup/teardown shared across tests ------------------
@pytest.fixture
def sample_services():
    """Provides test data; anything after `yield` is teardown."""
    data = [
        {"name": "auth", "healthy": True},
        {"name": "payments", "healthy": False},
    ]
    yield data
    # (teardown would go here, e.g. close a connection or delete temp files)


def test_uses_fixture(sample_services):
    unhealthy = [s["name"] for s in sample_services if not s["healthy"]]
    assert unhealthy == ["payments"]


# --- Testing that errors are raised correctly ------------------------------
def test_parse_cpu_rejects_garbage():
    with pytest.raises(ValueError):
        parse_cpu("not-a-number")
