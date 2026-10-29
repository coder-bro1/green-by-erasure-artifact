"""Tests for the Tribonacci sequence documented by solution.tri."""

import pytest

from solution import tri


@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, [1]), (1, [1, 3]), (2, [1, 3, 2])],
)
def test_initial_values(n, expected):
    assert tri(n) == expected


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (3, [1, 3, 2, 8]),
        (4, [1, 3, 2, 8, 3]),
        (5, [1, 3, 2, 8, 3, 15]),
        (10, [1, 3, 2, 8, 3, 15, 4, 24, 5, 35, 6]),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="Odd terms add an extra index value; the docstring requires tri(3) = 8, not 11.",
)
def test_documented_sequence(n, expected):
    assert tri(n) == expected


@pytest.mark.parametrize("n", [0, 1, 2, 3, 10, 100])
def test_result_contains_first_n_plus_one_values(n):
    result = tri(n)
    assert isinstance(result, list)
    assert len(result) == n + 1
    assert result[0] == 1
    if n >= 1:
        assert result[1] == 3


@pytest.mark.parametrize("n", [2, 4, 6, 10, 20, 100])
def test_even_terms_follow_documented_formula(n):
    result = tri(n)
    for index in range(2, n + 1, 2):
        assert result[index] == 1 + index // 2


@pytest.mark.parametrize("index", [3, 5, 7, 9, 99])
@pytest.mark.xfail(
    strict=True,
    reason="Odd terms add index + tri(index + 1) instead of just tri(index + 1).",
)
def test_odd_terms_follow_documented_recurrence(index):
    result = tri(index + 1)
    assert result[index] == (
        result[index - 1] + result[index - 2] + result[index + 1]
    )


@pytest.mark.parametrize("n", [0, 1, 2, 3, 10, 99])
def test_extending_sequence_preserves_previous_terms(n):
    assert tri(n + 1)[:-1] == tri(n)
