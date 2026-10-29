import pytest

from solution import count_nums


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], 0),
        ([-1, 11, -11], 1),
        ([1, 1, 2], 3),
    ],
)
def test_docstring_examples(numbers, expected):
    assert count_nums(numbers) == expected


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (0, 0),
        (1, 1),
        (9, 1),
        (10, 1),
        (1000, 1),
        (123, 1),
        (-1, 0),
        (-9, 0),
        (-10, 0),
        (-1000, 0),
        (-11, 0),  # -1 + 1 = 0: the threshold is strictly positive.
        (-12, 1),
        (-123, 1),  # Only the first digit is negative: -1 + 2 + 3 = 4.
        (-21, 0),
        (-22, 0),
        (-23, 1),
        (-901, 0),
        (-909, 0),
        (-919, 1),
        (10**100, 1),
        (-(10**100), 0),
        (-(10**100 + 2), 1),
    ],
)
def test_individual_digit_sums(number, expected):
    assert count_nums([number]) == expected


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([0, 0, 0], 0),
        ([-9, -10, -21, -22, -900], 0),
        ([1, 10, 100, -12, -123, -919], 6),
        ([0, -1, -11, -12, -21, -23, 10], 3),
        ([-12, -12, -11, -11, 0, 1, 1], 4),
    ],
)
def test_counts_all_qualifying_elements(numbers, expected):
    assert count_nums(numbers) == expected


def test_input_is_not_modified():
    numbers = [-123, 0, 10, -11, -123]
    original = numbers.copy()

    assert count_nums(numbers) == 3
    assert numbers == original
