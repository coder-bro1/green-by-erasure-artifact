"""Tests for solution.sqrt (Newton-Raphson square root).

Spec (from the docstring): for x >= 1 and epsilon > 0, sqrt(x, epsilon)
returns a float in [sqrt(x) - epsilon, sqrt(x) + epsilon].

KNOWN BUG in solution.py: the loop condition is
    while abs(x - approx) > epsilon
but it should be
    while abs(x - approx * approx) > epsilon
Because `approx` converges to sqrt(x), the loop only terminates when x is
within epsilon of sqrt(x), i.e. for x == 1 (or x very close to 1). For any
other input -- including the docstring example sqrt(2, 0.01) -- it loops
forever.

Every call is therefore executed in a subprocess with a timeout so the suite
can never hang. Spec cases the bug breaks are marked xfail(strict=True): they
are expected to fail now, and will turn into failures (prompting removal of
the marker) once solution.py is fixed.
"""

import math
import pathlib
import subprocess
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
TIMEOUT = 3  # seconds; a correct implementation finishes in microseconds

BUG = (
    "solution.py loop condition compares x to approx instead of approx**2, "
    "so it never terminates unless x is ~1"
)


class Timeout(Exception):
    pass


def run_sqrt(x, epsilon, timeout=TIMEOUT):
    """Call solution.sqrt(x, epsilon) in a fresh interpreter; return the float."""
    code = (
        "from solution import sqrt; "
        f"print(repr(sqrt({x!r}, {epsilon!r})))"
    )
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            cwd=HERE,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise Timeout(f"sqrt({x!r}, {epsilon!r}) did not return within {timeout}s")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr)
    return float(proc.stdout.strip())


def assert_within_spec(x, epsilon):
    result = run_sqrt(x, epsilon)
    assert isinstance(result, float)
    assert math.sqrt(x) - epsilon <= result <= math.sqrt(x) + epsilon


# --------------------------------------------------------------------------
# Inputs where the current implementation terminates and meets the spec
# --------------------------------------------------------------------------

@pytest.mark.parametrize("epsilon", [1.0, 0.5, 0.1, 0.01, 1e-3, 1e-6, 1e-9, 1e-12])
def test_x_equals_one_within_epsilon(epsilon):
    assert_within_spec(1, epsilon)


def test_x_equals_one_as_float():
    assert_within_spec(1.0, 0.01)


@pytest.mark.parametrize("x", [1.0001, 1.001, 1.005])
def test_x_close_to_one_within_epsilon(x):
    # |x - sqrt(x)| < 0.01 here, so the (buggy) stopping test can be satisfied.
    assert_within_spec(x, 0.01)


def test_tight_epsilon_converges_to_one():
    result = run_sqrt(1, 1e-12)
    assert result == pytest.approx(1.0, abs=1e-12)


def test_starting_guess_is_returned_when_already_close():
    # approx starts at x/2 == 1.0 for x == 2; |2 - 1| == 1 <= epsilon, so the
    # loop body never runs. 1.0 is within 1.5 of sqrt(2), so the spec holds.
    assert run_sqrt(2, 1.5) == 1.0
    assert_within_spec(2, 1.5)


def test_large_epsilon_returns_initial_guess():
    # With an epsilon larger than |x - x/2| the loop is skipped entirely.
    assert run_sqrt(10, 100.0) == 5.0


def test_returns_float_for_int_input():
    assert isinstance(run_sqrt(1, 0.1), float)


def test_hang_is_detected_by_harness():
    # Documents the bug directly: the docstring example does not return.
    with pytest.raises(Timeout):
        run_sqrt(2, 0.01, timeout=1)


# --------------------------------------------------------------------------
# Spec cases broken by the bug (expected to fail until solution.py is fixed)
# --------------------------------------------------------------------------

@pytest.mark.xfail(raises=Timeout, strict=True, reason=BUG)
def test_docstring_example():
    assert run_sqrt(2, 0.01) == pytest.approx(1.4166666666666665)


@pytest.mark.xfail(raises=Timeout, strict=True, reason=BUG)
@pytest.mark.parametrize(
    "x, epsilon",
    [
        (2, 0.01),
        (4, 0.01),
        (9, 1e-6),
        (10, 0.1),
        (100, 1e-6),
        (12345.678, 1e-6),
        (1e6, 1e-3),
    ],
)
def test_spec_general_inputs(x, epsilon):
    assert_within_spec(x, epsilon)


@pytest.mark.xfail(raises=Timeout, strict=True, reason=BUG)
@pytest.mark.parametrize("x", [4, 16, 25, 144])
def test_perfect_squares(x):
    assert run_sqrt(x, 1e-9) == pytest.approx(math.isqrt(x), abs=1e-9)
