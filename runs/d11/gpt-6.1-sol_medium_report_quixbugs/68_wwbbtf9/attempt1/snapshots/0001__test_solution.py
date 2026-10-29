"""Tests for the nonnegative-integer contract documented by bitcount."""

import subprocess
import sys
from pathlib import Path

import pytest

from solution import bitcount


def test_bitcount_zero():
    assert bitcount(0) == 0


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        pytest.param(1, 1, id="smallest-positive"),
        pytest.param(2, 1, id="even-power-of-two"),
        pytest.param(3, 2, id="two-set-bits"),
        pytest.param(42, 3, id="alternating-bits"),
        pytest.param(127, 7, id="docstring-127"),
        pytest.param(128, 1, id="docstring-128"),
        pytest.param(255, 8, id="eight-set-bits"),
        pytest.param(1 << 100, 1, id="large-power-of-two"),
        pytest.param((1 << 100) - 1, 100, id="large-all-set-bits"),
    ],
)
def test_bitcount_positive(n, expected):
    # Isolate calls so a nonterminating implementation cannot hang pytest.
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "from solution import bitcount; "
                "import sys; print(bitcount(int(sys.argv[1])))",
                str(n),
            ],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            timeout=2,
            check=True,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"bitcount({n}) did not terminate within 2 seconds")
    assert int(result.stdout.strip()) == expected
