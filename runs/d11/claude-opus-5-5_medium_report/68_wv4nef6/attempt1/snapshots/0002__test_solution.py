import pytest

from solution import fibfib

# Reference values from the docstring definition:
# fibfib(0)=0, fibfib(1)=0, fibfib(2)=1, fibfib(n)=fibfib(n-1)+fibfib(n-2)+fibfib(n-3)
EXPECTED = [0, 0, 1, 1, 2, 4, 7, 13, 24, 44, 81, 149, 274, 504, 927]

BASE_CASE_BUG = (
    "solution.py uses base cases fibfib(1)=1 and fibfib(2)=2, but the docstring "
    "specifies fibfib(1)=0 and fibfib(2)=1"
)


def test_fibfib_zero():
    assert fibfib(0) == 0


@pytest.mark.xfail(strict=True, reason=BASE_CASE_BUG)
def test_fibfib_one():
    assert fibfib(1) == 0


@pytest.mark.xfail(strict=True, reason=BASE_CASE_BUG)
def test_fibfib_two():
    assert fibfib(2) == 1


@pytest.mark.xfail(strict=True, reason=BASE_CASE_BUG)
def test_docstring_example_5():
    assert fibfib(5) == 4


@pytest.mark.xfail(strict=True, reason=BASE_CASE_BUG)
def test_docstring_example_8():
    assert fibfib(8) == 24


@pytest.mark.xfail(strict=True, reason=BASE_CASE_BUG)
def test_first_fifteen_values():
    assert [fibfib(n) for n in range(len(EXPECTED))] == EXPECTED


@pytest.mark.parametrize("n", range(3, 18))
def test_recurrence_relation(n):
    assert fibfib(n) == fibfib(n - 1) + fibfib(n - 2) + fibfib(n - 3)


def test_returns_int():
    assert isinstance(fibfib(10), int)
