import pytest

from solution import biggest_proper_factor


@pytest.mark.parametrize(
    "num, expected",
    [
        (21, 7),    # docstring example
        (32, 16),   # docstring example
        (2, 1),
        (7, 1),     # prime -> 1
        (97, 1),    # larger prime
        (9, 3),     # square of a prime
        (15, 5),
        (100, 50),
        (49, 7),
        (1001, 143),  # 7 * 11 * 13
    ],
)
def test_biggest_proper_factor(num, expected):
    assert biggest_proper_factor(num) == expected


@pytest.mark.parametrize("num", [2, 6, 12, 35, 64, 81, 360, 997])
def test_result_is_a_proper_divisor(num):
    result = biggest_proper_factor(num)
    assert isinstance(result, int)
    assert 1 <= result < num
    assert num % result == 0


@pytest.mark.parametrize("num", [2, 6, 12, 35, 64, 81, 360, 997])
def test_result_is_the_largest_proper_divisor(num):
    result = biggest_proper_factor(num)
    assert all(num % d != 0 for d in range(result + 1, num))
