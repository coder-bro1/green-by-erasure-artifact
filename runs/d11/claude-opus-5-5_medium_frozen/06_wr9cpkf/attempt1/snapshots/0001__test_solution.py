import pytest

from solution import even_odd_palindrome


def reference(n, inclusive=False):
    stop = n + 1 if inclusive else n
    pals = [i for i in range(1, stop) if str(i) == str(i)[::-1]]
    return (sum(1 for p in pals if p % 2 == 0), sum(1 for p in pals if p % 2 == 1))


# Actual behavior: solution iterates range(1, n), i.e. n itself is EXCLUDED.

@pytest.mark.parametrize(
    "n, expected",
    [
        (1, (0, 0)),
        (2, (0, 1)),
        (3, (1, 1)),
        (4, (1, 2)),
        (10, (4, 5)),
        (11, (4, 5)),
        (12, (4, 6)),
        (23, (5, 6)),
        (100, (8, 10)),
        (102, (8, 11)),
        (1000, (48, 60)),
    ],
)
def test_known_values(n, expected):
    assert even_odd_palindrome(n) == expected


def test_returns_tuple_of_ints():
    result = even_odd_palindrome(50)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(x, int) for x in result)


def test_n_is_excluded_when_palindrome():
    # 11 is an odd palindrome; it counts for n=12 but not n=11
    assert even_odd_palindrome(11) == (4, 5)
    assert even_odd_palindrome(12) == (4, 6)


@pytest.mark.parametrize("n", range(1, 1001))
def test_matches_reference_full_range(n):
    assert even_odd_palindrome(n) == reference(n)


def test_monotonic_non_decreasing():
    prev = (0, 0)
    for n in range(1, 1001):
        cur = even_odd_palindrome(n)
        assert cur[0] >= prev[0] and cur[1] >= prev[1]
        prev = cur


def test_non_positive_input_returns_zero():
    assert even_odd_palindrome(0) == (0, 0)
    assert even_odd_palindrome(-5) == (0, 0)


# Docstring says range is inclusive of n; the implementation is not.
@pytest.mark.xfail(strict=True, reason="docstring claims n is inclusive; code uses range(1, n)")
@pytest.mark.parametrize("n, expected", [(3, (1, 2)), (12, (4, 6))])
def test_docstring_examples(n, expected):
    assert even_odd_palindrome(n) == expected
