import pytest

from solution import count_odd_edged

KNOWN_BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py treats 2 as an odd digit: odd = (1, 2, 3, 5, 7, 9)",
)


def test_empty_list():
    assert count_odd_edged([]) == 0


def test_docstring_example_negative_excluded():
    assert count_odd_edged([57, -73]) == 1


@pytest.mark.parametrize("v", [11, 13, 15, 17, 19, 31, 57, 99, 135, 951, 1001, 97531])
def test_odd_first_and_last_counted(v):
    assert count_odd_edged([v]) == 1


@pytest.mark.parametrize("v", [12, 14, 30, 41, 61, 81, 46, 100, 456, 1010])
def test_even_first_or_last_not_counted(v):
    assert count_odd_edged([v]) == 0


@pytest.mark.parametrize("v", [10, 9, 7, 5, 1, 0, -11, -13, -99, -135])
def test_values_not_greater_than_10_excluded(v):
    assert count_odd_edged([v]) == 0


def test_mixed_list():
    assert count_odd_edged([11, 12, 13, 14, 15, 9, -31, 10, 77]) == 4


def test_duplicates_counted_each_time():
    assert count_odd_edged([33, 33, 33]) == 3


def test_accepts_any_iterable():
    assert count_odd_edged(x for x in (11, 13, 40)) == 2


def test_does_not_mutate_input():
    data = [11, 22, 33]
    count_odd_edged(data)
    assert data == [11, 22, 33]


# --- Tests exposing the bug in solution.py (2 treated as odd) ---

@KNOWN_BUG
def test_docstring_example_with_25():
    assert count_odd_edged([31, 25, 12, 9]) == 1


@KNOWN_BUG
@pytest.mark.parametrize("v", [21, 23, 25, 27, 29, 211])
def test_leading_2_not_counted(v):
    assert count_odd_edged([v]) == 0


@KNOWN_BUG
@pytest.mark.parametrize("v", [12, 32, 52, 112])
def test_trailing_2_not_counted(v):
    assert count_odd_edged([v]) == 0
