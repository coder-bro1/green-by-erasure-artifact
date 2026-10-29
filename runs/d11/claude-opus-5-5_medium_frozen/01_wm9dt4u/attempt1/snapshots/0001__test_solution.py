"""Tests for solution.tri.

The docstring defines (with tri(0) = 1 as shown by the example):
    tri(1) = 3
    tri(n) = 1 + n / 2                          if n is even
    tri(n) = tri(n-1) + tri(n-2) + tri(n+1)     if n is odd
and tri(n) must return the first n + 1 terms.

The current implementation adds an extra ``i`` in the odd branch, so odd
terms from index 3 onward are wrong (tri(3) gives [1, 3, 2, 11] instead of
[1, 3, 2, 8]). Those spec checks are marked xfail(strict=True): they
document the bug, and the suite will fail loudly once it is fixed so the
markers can be removed.
"""

import pytest

from solution import tri


def reference_tri(n):
    """Straightforward implementation of the documented recurrence."""
    def term(k):
        if k == 0:
            return 1
        if k == 1:
            return 3
        if k % 2 == 0:
            return 1 + k / 2
        return term(k - 1) + term(k - 2) + term(k + 1)

    return [term(k) for k in range(n + 1)]


# --- Behaviour the implementation gets right -------------------------------

def test_zero_returns_single_element():
    assert tri(0) == [1]


def test_one():
    assert tri(1) == [1, 3]


def test_two():
    assert tri(2) == [1, 3, 2]


@pytest.mark.parametrize("n", range(0, 30))
def test_length_is_n_plus_one(n):
    assert len(tri(n)) == n + 1


@pytest.mark.parametrize("n", range(1, 30))
def test_first_two_terms_fixed(n):
    result = tri(n)
    assert result[0] == 1
    assert result[1] == 3


@pytest.mark.parametrize("n", [2, 5, 10, 25])
def test_even_index_terms_follow_formula(n):
    result = tri(n)
    for k in range(2, n + 1, 2):
        assert result[k] == 1 + k / 2


@pytest.mark.parametrize("n", [3, 8, 20])
def test_prefix_consistency(n):
    """tri(m) is a prefix of tri(n) for every m <= n."""
    full = tri(n)
    for m in range(n + 1):
        assert tri(m) == full[: m + 1]


def test_returns_new_list_each_call():
    a = tri(4)
    a.append("x")
    assert tri(4) == a[:-1]


def test_reference_matches_docstring_examples():
    # Sanity-check the oracle used by the xfail tests below.
    assert reference_tri(3) == [1, 3, 2, 8]
    assert reference_tri(4)[4] == 3


# --- Documented behaviour the implementation currently violates ------------

BUG = "solution.py adds an extra `i` to odd terms (tri(3) -> 11, expected 8)"


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example_tri_3():
    assert tri(3) == [1, 3, 2, 8]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_tri_4_list():
    assert tri(4) == [1, 3, 2, 8, 3]


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("n", [5, 10, 20])
def test_matches_reference_recurrence(n):
    assert tri(n) == reference_tri(n)
