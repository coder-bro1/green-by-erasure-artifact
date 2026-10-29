from math import comb

import pytest

from solution import pascal


@pytest.mark.parametrize("n", [1, 2, 3, 5, 10, 20])
def test_returns_first_n_rows_of_pascals_triangle(n):
    expected = [[comb(row, column) for column in range(row + 1)] for row in range(n)]

    assert pascal(n) == expected


def test_docstring_example():
    assert pascal(5) == [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
    ]


def test_single_row_is_a_list_of_lists():
    result = pascal(1)

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], list)
    assert result[0] == [1]


def test_calls_return_independent_rows():
    first = pascal(1)
    second = pascal(1)

    first[0][0] = 99
    first.append([2])

    assert second == [[1]]
    assert pascal(1) == [[1]]
