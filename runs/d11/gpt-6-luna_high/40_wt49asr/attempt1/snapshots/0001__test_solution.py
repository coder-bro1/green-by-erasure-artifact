import pytest

from solution import largest_divisor


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (2, 1),  # smallest supported input
        (7, 1),  # prime numbers have no proper divisor other than 1
        (12, 6),
        (15, 5),  # example from the function's docstring
        (36, 18),
        (100, 50),
    ],
)
def test_largest_divisor(number: int, expected: int) -> None:
    assert largest_divisor(number) == expected


@pytest.mark.parametrize("number", [2, 3, 4, 12, 15, 36, 100])
def test_result_is_a_proper_divisor(number: int) -> None:
    result = largest_divisor(number)

    assert 1 <= result < number
    assert number % result == 0
