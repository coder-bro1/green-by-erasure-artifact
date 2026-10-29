import pytest

from solution import next_palindrome


ALL_NINES_REASON = (
    "For an all-9 palindrome, solution.py inserts one extra zero: "
    "9 should become 11, and 99 should become 101."
)


def digits(number):
    return [int(digit) for digit in str(number)]


# Enumerate integers independently of the implementation to obtain consecutive
# palindromes, including the successor of the largest four-digit palindrome.
SMALL_PALINDROMES = [
    number for number in range(10_002) if str(number) == str(number)[::-1]
]
SMALL_CASES = [
    pytest.param(
        current,
        following,
        id=str(current),
        marks=(
            pytest.mark.xfail(strict=True, reason=ALL_NINES_REASON)
            if set(str(current)) == {"9"}
            else ()
        ),
    )
    for current, following in zip(SMALL_PALINDROMES, SMALL_PALINDROMES[1:])
]


@pytest.mark.parametrize("current, expected", SMALL_CASES)
def test_next_palindrome_for_every_palindrome_below_10000(current, expected):
    assert next_palindrome(digits(current)) == digits(expected)


def test_docstring_example():
    assert next_palindrome([1, 4, 9, 4, 1]) == [1, 5, 0, 5, 1]


@pytest.mark.parametrize(
    "current, expected",
    [
        (12321, 12421),
        (123321, 124421),
        (12921, 13031),
        (129921, 130031),
        (19991, 20002),
        (199991, 200002),
        (9998999, 9999999),
        (100000000000000000001, 100000000010000000001),
    ],
)
def test_larger_palindromes_and_carries(current, expected):
    assert next_palindrome(digits(current)) == digits(expected)


@pytest.mark.xfail(strict=True, reason=ALL_NINES_REASON)
@pytest.mark.parametrize("length", [5, 6, 20, 21])
def test_all_nines_grows_by_one_digit(length):
    expected = [1] + [0] * (length - 1) + [1]
    assert next_palindrome([9] * length) == expected
