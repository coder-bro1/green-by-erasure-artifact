"""Regression tests for the current implementation of solution.tri.

The implementation's odd terms differ from the recurrence in its docstring.
These tests preserve the implemented behavior without changing solution.py.
"""

import pytest

from solution import tri


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, [1]),
        (1, [1, 3]),
        (2, [1, 3, 2]),
        (3, [1, 3, 2, 11]),
        (4, [1, 3, 2, 11, 3]),
        (5, [1, 3, 2, 11, 3, 23]),
        (8, [1, 3, 2, 11, 3, 23, 4, 39, 5]),
    ],
)
def test_known_sequences(n, expected):
    assert tri(n) == expected


@pytest.mark.parametrize("n", [0, 1, 2, 3, 10, 31, 100, 1000])
def test_terms_match_independent_closed_form(n):
    # The implemented odd-term recurrence simplifies to (i**2 + 4*i + 1)/2.
    expected = [
        1 if i == 0 else (i // 2 + 1 if i % 2 == 0 else (i * i + 4 * i + 1) // 2)
        for i in range(n + 1)
    ]
    result = tri(n)
    assert isinstance(result, list)
    assert len(result) == n + 1
    assert result == expected


@pytest.mark.parametrize("n", [0, 1, 2, 5, 20])
def test_extending_sequence_preserves_prefix(n):
    assert tri(n + 1)[:-1] == tri(n)


def test_calls_return_independent_lists():
    first = tri(5)
    second = tri(5)
    assert first is not second
    first[0] = -100
    first.append(999)
    assert second == [1, 3, 2, 11, 3, 23]
    assert tri(5) == second
