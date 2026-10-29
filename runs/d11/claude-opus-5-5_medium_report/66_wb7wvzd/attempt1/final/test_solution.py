import pytest

from solution import even_odd_palindrome


def _reference(n):
    even = odd = 0
    for i in range(1, n + 1):
        s = str(i)
        if s == s[::-1]:
            if i % 2 == 0:
                even += 1
            else:
                odd += 1
    return (even, odd)


@pytest.mark.parametrize(
    "n, expected",
    [
        (3, (1, 2)),       # docstring example 1
        (12, (4, 6)),      # docstring example 2
        (1, (0, 1)),       # lower bound
        (2, (1, 1)),
        (9, (4, 5)),
        (10, (4, 5)),      # 10 is not a palindrome
        (11, (4, 6)),      # n itself is included
        (22, (5, 6)),
        (99, (8, 10)),
        (100, (8, 10)),
        (101, (8, 11)),
        (121, (8, 13)),
        (191, (8, 20)),
        (202, (9, 20)),
        (1000, (48, 60)),  # upper bound: 9 + 9 + 90 palindromes
    ],
)
def test_known_values(n, expected):
    assert even_odd_palindrome(n) == expected


def test_returns_tuple_of_ints():
    result = even_odd_palindrome(50)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(x, int) for x in result)


@pytest.mark.parametrize("n", range(1, 1001))
def test_matches_reference_over_full_domain(n):
    assert even_odd_palindrome(n) == _reference(n)


def test_monotonic_non_decreasing():
    prev = (0, 0)
    for n in range(1, 1001):
        cur = even_odd_palindrome(n)
        assert cur[0] >= prev[0] and cur[1] >= prev[1]
        assert sum(cur) - sum(prev) in (0, 1)
        prev = cur
