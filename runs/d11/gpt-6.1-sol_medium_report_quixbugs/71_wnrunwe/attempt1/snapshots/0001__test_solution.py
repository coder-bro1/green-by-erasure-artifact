from math import comb

import pytest

from solution import pascal


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, [[1]]),
        (2, [[1], [1, 1]]),
        (3, [[1], [1, 1], [1, 2, 1]]),
        (5, [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]),
    ],
)
def test_pascal_known_rows(n, expected):
    """Cover the minimum valid input and the documented example."""
    assert pascal(n) == expected


@pytest.mark.parametrize("n", [4, 6, 10, 25, 50])
def test_pascal_matches_binomial_coefficients(n):
    """Use an independent mathematical oracle for every returned entry."""
    rows = pascal(n)

    assert isinstance(rows, list)
    assert len(rows) == n
    for index, row in enumerate(rows):
        assert isinstance(row, list)
        assert len(row) == index + 1
        assert all(type(value) is int for value in row)
        assert row == [comb(index, column) for column in range(index + 1)]


def test_pascal_returns_independent_rows_and_results():
    rows = pascal(5)
    rows[0][0] = 99
    rows[1].append(99)

    assert rows[2:] == [[1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    assert pascal(2) == [[1], [1, 1]]
