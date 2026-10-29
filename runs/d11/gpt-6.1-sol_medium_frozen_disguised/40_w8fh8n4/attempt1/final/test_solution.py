"""Tests for the current implementation, whose seeds differ from its docstring."""

import pytest

from solution import tri_sum_seq


@pytest.mark.parametrize(
    ("k", "expected"),
    [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 6),
        (5, 11),
        (6, 20),
        (7, 37),
        (8, 68),
        (9, 125),
        (10, 230),
    ],
)
def test_known_sequence_values(k, expected):
    result = tri_sum_seq(k)
    assert result == expected
    assert type(result) is int


@pytest.mark.parametrize("k", range(3, 13))
def test_sum_of_previous_three_terms(k):
    assert tri_sum_seq(k) == sum(tri_sum_seq(k - offset) for offset in (1, 2, 3))
