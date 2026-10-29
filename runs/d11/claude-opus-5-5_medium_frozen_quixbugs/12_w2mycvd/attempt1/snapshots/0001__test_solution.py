"""Tests for solution.bitcount.

NOTE: solution.py has a known bug: the loop body uses ``n ^= n - 1`` instead of
``n &= n - 1``. For any n > 0, n eventually becomes 1 and ``1 ^ 0 == 1``, so the
loop never terminates. Each call therefore runs in a subprocess with a timeout,
and the n > 0 cases are marked as strict xfail. When the bug is fixed they will
XPASS, and strict mode turns that into a failure so the markers get removed.
"""
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
TIMEOUT = 3  # seconds


def run_bitcount(n):
    """Call bitcount(n) in a fresh interpreter. Returns int result, or None on timeout."""
    code = f"from solution import bitcount; print(bitcount({n!r}))"
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            cwd=HERE,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None
    assert proc.returncode == 0, proc.stderr
    return int(proc.stdout.strip())


def test_zero_has_no_set_bits():
    assert run_bitcount(0) == 0


def test_zero_in_process():
    # n == 0 never enters the loop, so it is safe to call directly.
    from solution import bitcount

    assert bitcount(0) == 0
    assert isinstance(bitcount(0), int)


BUG = "solution.py uses `n ^= n - 1` instead of `n &= n - 1`; loops forever for n > 0"


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize(
    "n, expected",
    [
        (127, 7),  # docstring example
        (128, 1),  # docstring example
        (1, 1),
        (2, 1),
        (3, 2),
        (255, 8),
        (1023, 10),
        (0b1010101, 4),
        (2**64, 1),
        (2**64 - 1, 64),
    ],
)
def test_bitcount_positive(n, expected):
    assert run_bitcount(n) == expected


def test_positive_input_currently_hangs():
    """Pins down the current (buggy) behavior: bitcount(1) does not return."""
    assert run_bitcount(1) is None
