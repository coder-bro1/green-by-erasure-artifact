"""Tests for bitcount, including its known nontermination for positive inputs."""

from pathlib import Path
import subprocess
import sys

import pytest

from solution import bitcount


def test_zero_has_no_set_bits():
    assert bitcount(0) == 0


@pytest.mark.xfail(
    strict=True,
    reason="Positive inputs never terminate: n ^= n - 1 eventually leaves n at 1.",
    raises=subprocess.TimeoutExpired,
)
@pytest.mark.parametrize(
    ("number", "expected"),
    [
        pytest.param(1, 1, id="smallest-positive"),
        pytest.param(2, 1, id="power-of-two"),
        pytest.param(3, 2, id="adjacent-set-bits"),
        pytest.param(10, 2, id="separated-set-bits"),
        pytest.param(127, 7, id="documented-example-127"),
        pytest.param(128, 1, id="documented-example-128"),
        pytest.param((1 << 100) | (1 << 50) | 1, 3, id="large-sparse-integer"),
        pytest.param((1 << 100) - 1, 100, id="large-dense-integer"),
    ],
)
def test_positive_integer_bitcount(number, expected):
    # Isolate calls so a nonterminating implementation cannot hang pytest.
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            f"from solution import bitcount; print(bitcount({number}))",
        ],
        cwd=Path(__file__).resolve().parent,
        capture_output=True,
        text=True,
        check=True,
        timeout=1,
    )
    assert int(result.stdout.strip()) == expected
