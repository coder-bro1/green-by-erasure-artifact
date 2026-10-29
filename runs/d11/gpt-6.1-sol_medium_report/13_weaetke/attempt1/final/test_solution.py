"""Tests for the sequence and return value documented by solution.tri."""

import pytest

from solution import tri


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, [1]),
        (1, [1, 3]),
        (2, [1, 3, 2]),
        (3, [1, 3, 2, 8]),  # The docstring's worked example.
        (4, [1, 3, 2, 8, 3]),
        (5, [1, 3, 2, 8, 3, 15]),
        (10, [1, 3, 2, 8, 3, 15, 4, 24, 5, 35, 6]),
    ],
)
def test_documented_sequence_values(n, expected):
    assert tri(n) == expected


@pytest.mark.parametrize("n", [0, 1, 2, 3, 10, 31, 100])
def test_returns_list_of_first_n_plus_one_terms(n):
    result = tri(n)

    assert isinstance(result, list)
    assert len(result) == n + 1
    assert result[0] == 1
    if n >= 1:
        assert result[1] == 3


@pytest.mark.parametrize("n", [2, 3, 4, 5, 20, 31, 100])
def test_terms_obey_documented_recurrence(n):
    # Include the next term because the odd-index recurrence uses tri(i + 1).
    result = tri(n + 1)

    for i in range(2, n + 1):
        if i % 2 == 0:
            assert result[i] == 1 + i // 2
        else:
            assert result[i] == result[i - 1] + result[i - 2] + result[i + 1]


@pytest.mark.parametrize("n", [0, 1, 2, 3, 10, 31])
def test_shorter_result_is_prefix_of_longer_sequence(n):
    assert tri(n) == tri(n + 5)[: n + 1]
