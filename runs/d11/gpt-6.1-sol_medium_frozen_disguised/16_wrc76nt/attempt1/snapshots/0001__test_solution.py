"""Regression tests for the current implementation of odd_even_series.

The odd-index outputs differ from the recurrence and example in the docstring.
These tests preserve the implementation's behavior without changing solution.py.
"""

import pytest

from solution import odd_even_series


@pytest.mark.parametrize(
    ("count", "expected"),
    [
        (0, [1]),
        (1, [1, 3]),
        (2, [1, 3, 2.0]),
        (3, [1, 3, 2.0, 11.0]),
        (5, [1, 3, 2.0, 11.0, 3.0, 22.0]),
        (8, [1, 3, 2.0, 11.0, 3.0, 22.0, 4.0, 37.0, 5.0]),
        (9, [1, 3, 2.0, 11.0, 3.0, 22.0, 4.0, 37.0, 5.0, 56.0]),
    ],
)
def test_known_sequences(count, expected):
    assert odd_even_series(count) == expected


@pytest.mark.parametrize("count", [0, 1, 2, 3, 10, 99, 100, 1000])
def test_length_and_index_values(count):
    sequence = odd_even_series(count)

    assert isinstance(sequence, list)
    assert len(sequence) == count + 1
    assert sequence[0] == 1
    if count >= 1:
        assert sequence[1] == 3

    for index in range(2, count + 1):
        if index % 2 == 0:
            assert sequence[index] == 1 + index / 2
        else:
            # Closed form of the implementation's odd-index recurrence.
            # For index = 2m + 1, the value is 2m**2 + 6m + 3.
            m = (index - 1) // 2
            assert sequence[index] == 2 * m**2 + 6 * m + 3


def test_shorter_sequence_is_prefix_of_longer_sequence():
    longer = odd_even_series(30)
    for count in range(31):
        assert odd_even_series(count) == longer[: count + 1]


def test_calls_return_independent_lists():
    first = odd_even_series(5)
    second = odd_even_series(5)

    assert first is not second
    first[0] = -1
    first.append(999)

    assert second == [1, 3, 2.0, 11.0, 3.0, 22.0]
    assert odd_even_series(5) == second
