import pytest

from solution import tri

ODD_BUG = (
    "solution.py adds an extra '+ i' term for odd n "
    "(my_tri[i-1] + my_tri[i-2] + i + (i+3)/2), so tri(3) is 11 instead of the "
    "documented 2 + 3 + 3 = 8"
)


def test_zero_returns_single_element():
    assert tri(0) == [1]


def test_one():
    assert tri(1) == [1, 3]


def test_two_even_term():
    assert tri(2) == [1, 3, 2]


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 7, 10])
def test_length_is_n_plus_one(n):
    assert len(tri(n)) == n + 1


@pytest.mark.parametrize("n", [2, 4, 6, 8, 10])
def test_even_terms_follow_formula(n):
    result = tri(10)
    assert result[n] == 1 + n / 2


def test_prefix_consistency():
    # Each shorter result is a prefix of a longer one
    long = tri(9)
    for n in range(10):
        assert tri(n) == long[: n + 1]


@pytest.mark.xfail(strict=True, reason=ODD_BUG)
def test_docstring_example():
    assert tri(3) == [1, 3, 2, 8]


@pytest.mark.xfail(strict=True, reason=ODD_BUG)
def test_four():
    assert tri(4) == [1, 3, 2, 8, 3]


@pytest.mark.xfail(strict=True, reason=ODD_BUG)
def test_five():
    # tri(5) = tri(4) + tri(3) + tri(6) = 3 + 8 + 4 = 15
    assert tri(5) == [1, 3, 2, 8, 3, 15]


@pytest.mark.xfail(strict=True, reason=ODD_BUG)
def test_seven():
    # tri(7) = tri(6) + tri(5) + tri(8) = 4 + 15 + 5 = 24
    assert tri(7) == [1, 3, 2, 8, 3, 15, 4, 24]


@pytest.mark.xfail(strict=True, reason=ODD_BUG)
@pytest.mark.parametrize("n", [3, 5, 7, 9])
def test_odd_terms_follow_recurrence(n):
    result = tri(n + 1)
    expected = result[n - 1] + result[n - 2] + (1 + (n + 1) / 2)
    assert result[n] == expected
