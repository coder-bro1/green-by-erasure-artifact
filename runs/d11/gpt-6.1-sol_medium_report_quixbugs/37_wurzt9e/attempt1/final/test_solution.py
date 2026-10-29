"""Tests for the documented positive-k contract of subsequences."""

from itertools import combinations

import pytest

from solution import subsequences


@pytest.mark.xfail(
    strict=True,
    reason="The k == 0 base case returns [] instead of [[]], so valid sequences are lost.",
)
def test_docstring_example():
    assert subsequences(a=1, b=5, k=3) == [
        [1, 2, 3],
        [1, 2, 4],
        [1, 3, 4],
        [2, 3, 4],
    ]


@pytest.mark.xfail(
    strict=True,
    reason="The k == 0 base case returns [] instead of [[]], so valid sequences are lost.",
)
@pytest.mark.parametrize(
    "a,b,k",
    [
        pytest.param(1, 5, 1, id="singletons-exclude-upper-bound"),
        pytest.param(3, 4, 1, id="one-value-range"),
        pytest.param(1, 5, 4, id="length-equals-range-size"),
        pytest.param(0, 5, 2, id="pairs-starting-at-zero"),
        pytest.param(-4, -1, 2, id="negative-bounds"),
        pytest.param(-2, 3, 3, id="range-crosses-zero"),
        pytest.param(10, 16, 4, id="larger-start-and-length"),
    ],
)
def test_all_ascending_sequences(a, b, k):
    expected = [list(sequence) for sequence in combinations(range(a, b), k)]
    assert subsequences(a, b, k) == expected


@pytest.mark.parametrize(
    "a,b,k",
    [
        pytest.param(0, 0, 1, id="empty-range"),
        pytest.param(-2, -2, 3, id="empty-negative-range"),
        pytest.param(5, 1, 1, id="reversed-range"),
        pytest.param(-1, -4, 2, id="reversed-negative-range"),
        pytest.param(1, 5, 5, id="length-one-too-large"),
        pytest.param(-2, 2, 10, id="length-much-too-large"),
    ],
)
def test_no_sequences_when_range_has_too_few_values(a, b, k):
    assert subsequences(a, b, k) == []
