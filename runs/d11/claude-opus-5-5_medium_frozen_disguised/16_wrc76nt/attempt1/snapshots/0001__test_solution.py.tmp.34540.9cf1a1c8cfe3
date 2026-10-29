import pytest

from solution import odd_even_series

BUG = (
    "solution.py odd-k branch adds an extra '+ k' term "
    "(computes t(k-1) + t(k-2) + k + t(k+1) instead of t(k-1) + t(k-2) + t(k+1))"
)


def reference(count):
    """Independent implementation of the documented recurrence."""
    def even(k):
        return 1 + k / 2

    t = [1, 3]
    for k in range(2, count + 1):
        if k % 2 == 0:
            t.append(even(k))
        else:
            t.append(t[k - 1] + t[k - 2] + even(k + 1))
    return t[: count + 1]


# ---- behaviour that matches the spec ----

def test_count_zero():
    assert odd_even_series(0) == [1]


def test_count_one():
    assert odd_even_series(1) == [1, 3]


def test_count_two():
    assert odd_even_series(2) == [1, 3, 2.0]


@pytest.mark.parametrize("count", [0, 1, 2, 5, 10, 25])
def test_length_is_count_plus_one(count):
    assert len(odd_even_series(count)) == count + 1


@pytest.mark.parametrize("count", [2, 6, 11, 30])
def test_even_indices_follow_even_rule(count):
    result = odd_even_series(count)
    for k in range(2, count + 1, 2):
        assert result[k] == 1 + k / 2


def test_first_two_terms_are_fixed():
    for count in range(1, 10):
        assert odd_even_series(count)[:2] == [1, 3]


def test_even_terms_are_floats():
    result = odd_even_series(8)
    for k in range(2, 9, 2):
        assert isinstance(result[k], float)


def test_prefix_consistency():
    # A longer series must extend a shorter one.
    long = odd_even_series(20)
    for n in range(21):
        assert odd_even_series(n) == long[: n + 1]


# ---- odd rule (k >= 3): currently broken in solution.py ----

@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example():
    assert odd_even_series(5) == [1, 3, 2.0, 8.0, 3.0, 15.0]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_t3():
    # t(3) = t(2) + t(1) + t(4) = 2 + 3 + 3 = 8
    assert odd_even_series(3)[3] == 8.0


@pytest.mark.xfail(strict=True, reason=BUG)
def test_odd_indices_follow_odd_rule():
    result = odd_even_series(15)
    for k in range(3, 16, 2):
        assert result[k] == result[k - 1] + result[k - 2] + (1 + (k + 1) / 2)


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("count", [3, 7, 12, 20])
def test_matches_reference(count):
    assert odd_even_series(count) == reference(count)


def test_reference_matches_docstring():
    # Sanity check for the reference implementation used above.
    assert reference(0) == [1]
    assert reference(5) == [1, 3, 2.0, 8.0, 3.0, 15.0]
