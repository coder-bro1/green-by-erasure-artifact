import pytest

from solution import weave_separator


@pytest.mark.parametrize(
    "values, sep, expected",
    [
        ([7, 8], 0, [7, 0, 8]),
        ([5, 5, 5], -1, [5, -1, 5, -1, 5]),
        ([], 2, []),
        ([42], 9, [42]),
        ([1, 2, 3, 4], 0, [1, 0, 2, 0, 3, 0, 4]),
        ([0, 0], 0, [0, 0, 0]),
    ],
)
def test_weave_separator(values, sep, expected):
    assert weave_separator(values, sep) == expected


def test_length_is_2n_minus_1():
    for n in range(1, 10):
        assert len(weave_separator(list(range(n)), -1)) == 2 * n - 1


def test_does_not_mutate_input_and_returns_new_list():
    values = [1, 2, 3]
    result = weave_separator(values, 0)
    assert values == [1, 2, 3]
    assert result is not values
