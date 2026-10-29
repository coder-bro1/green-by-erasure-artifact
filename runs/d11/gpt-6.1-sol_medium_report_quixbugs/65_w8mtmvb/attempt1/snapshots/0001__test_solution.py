"""Tests for sqrt's documented behavior on inputs meeting its precondition."""

import json
import math
from pathlib import Path
import subprocess
import sys

import pytest


def run_sqrt(x, epsilon):
    """Isolate calls so a nonterminating implementation cannot hang pytest."""
    script = (
        "import json, sys; from solution import sqrt; "
        "print(json.dumps(sqrt(float(sys.argv[1]), float(sys.argv[2]))))"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", script, str(x), str(epsilon)],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            check=True,
            timeout=2,
        )
    except subprocess.TimeoutExpired as exc:
        raise AssertionError(
            f"sqrt({x}, {epsilon}) did not return within two seconds"
        ) from exc
    return json.loads(result.stdout)


@pytest.mark.parametrize(
    ("x", "epsilon"),
    [
        (1.0, 0.5),  # Lower endpoint of the promised interval.
        (1.0, 0.3),
        (2.0, 0.6),
        (2.25, 1.125),
        (4.0, 2.0),  # Exact square root at the initial estimate.
        (9.0, 5.0),
        (16.0, 8.0),
        (100.0, 50.0),
        (1_000_000.0, 500_000.0),
    ],
)
def test_sqrt_returns_float_in_documented_interval(x, epsilon):
    result = run_sqrt(x, epsilon)

    assert isinstance(result, float)
    assert math.sqrt(x) - epsilon <= result <= math.sqrt(x) + epsilon


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Stopping condition compares the estimate with x, causing nontermination",
)
@pytest.mark.parametrize(("x", "epsilon"), [(1.0, 0.001), (4.0, 0.001), (9.0, 0.001)])
def test_sqrt_with_small_positive_tolerance(x, epsilon):
    result = run_sqrt(x, epsilon)

    assert isinstance(result, float)
    assert math.sqrt(x) - epsilon <= result <= math.sqrt(x) + epsilon


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Stopping condition can return an estimate outside the documented interval",
)
@pytest.mark.parametrize(("x", "epsilon"), [(1.1, 0.2), (1.21, 0.1)])
def test_sqrt_fractional_inputs_respect_error_bound(x, epsilon):
    result = run_sqrt(x, epsilon)

    assert math.sqrt(x) - epsilon <= result <= math.sqrt(x) + epsilon


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="The docstring example loops forever because the estimate never approaches x",
)
def test_sqrt_docstring_example():
    assert run_sqrt(2.0, 0.01) == 1.4166666666666665
