"""Characterize current behavior and expose the known factor calculation defect."""

import pytest

from solution import biggest_proper_factor


@pytest.mark.parametrize("num", [-10, -1, 0, 1, 2, 7, 9, 21, 32, 49, 100])
def test_current_implementation_returns_none(num):
    """The current loop never reaches its return statement for integer inputs."""
    assert biggest_proper_factor(num) is None


@pytest.mark.xfail(
    strict=True,
    reason="Known defect: num - d is never zero for d in range(num).",
)
@pytest.mark.parametrize(
    ("num", "expected"),
    [
        pytest.param(21, 7, id="documented-example-21"),
        pytest.param(32, 16, id="documented-example-32"),
        pytest.param(2, 1, id="smallest-prime"),
        pytest.param(3, 1, id="odd-prime"),
        pytest.param(97, 1, id="larger-prime"),
        pytest.param(4, 2, id="smallest-composite"),
        pytest.param(9, 3, id="odd-square"),
        pytest.param(49, 7, id="prime-square"),
        pytest.param(27, 9, id="odd-prime-power"),
        pytest.param(45, 15, id="odd-composite"),
        pytest.param(100, 50, id="even-composite"),
    ],
)
def test_largest_proper_factor_contract(num, expected):
    """Expected mathematical results; strict xfail keeps the defect visible."""
    assert biggest_proper_factor(num) == expected
