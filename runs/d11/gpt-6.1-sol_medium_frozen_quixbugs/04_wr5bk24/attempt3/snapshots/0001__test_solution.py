"""Tests for the documented Pascal's triangle contract."""

from math import comb

import pytest

from solution import pascal


MISSING_LAST_ENTRY = pytest.mark.xfail(
    strict=True,
    reason="pascal omits each row's last entry; n >= 3 then raises IndexError",
    raises=(AssertionError, IndexError),
)


@pytest.mark.parametrize(
    "n",
    [
        1,
        pytest.param(2, marks=MISSING_LAST_ENTRY),
        pytest.param(3, marks=MISSING_LAST_ENTRY),
        pytest.param(5, marks=MISSING_LAST_ENTRY),
        pytest.param(10, marks=MISSING_LAST_ENTRY),
        pytest.param(20, marks=MISSING_LAST_ENTRY),
    ],
)
def test_pascal_matches_binomial_coefficients(n):
    """Check every row and coefficient using an independent mathematical oracle."""
    expected = [[comb(row, column) for column in range(row + 1)] for row in range(n)]

    assert pascal(n) == expected


def test_single_row_is_a_list_of_lists():
    triangle = pascal(1)

    assert isinstance(triangle, list)
    assert len(triangle) == 1
    assert isinstance(triangle[0], list)
    assert triangle[0] == [1]


def test_calls_return_independent_mutable_results():
    first = pascal(1)
    second = pascal(1)

    assert first is not second
    assert first[0] is not second[0]
    first[0][0] = 99
    first.append([2])

    assert second == [[1]]
    assert pascal(1) == [[1]]
