import pytest

from solution import total_and_multiple


# --- Sum component -----------------------------------------------------------

@pytest.mark.parametrize(
    "values, expected_sum",
    [
        ([], 0),
        ([7], 7),
        ([2, 5], 7),
        ([-3, 4, 1], 2),
        ([0, 0, 0], 0),
        ([-1, -2, -3], -6),
        ([10**18, 10**18], 2 * 10**18),
    ],
)
def test_sum(values, expected_sum):
    assert total_and_multiple(values)[0] == expected_sum


# --- Product component -------------------------------------------------------

@pytest.mark.parametrize(
    "values, expected_product",
    [
        ([], 1),
        ([7], 7),
        ([2, 5], 10),
        ([-3, 4, 1], -12),
        ([-2, -3], 6),
        ([1, 2, 0, 4], 0),
        ([10**10, 10**10], 10**20),
    ],
)
def test_product(values, expected_product):
    assert total_and_multiple(values)[1] == expected_product


# --- Full return value / docstring examples ----------------------------------

@pytest.mark.parametrize(
    "values, expected",
    [
        ([2, 5], (7, 10)),
        ([-3, 4, 1], (2, -12)),
        ([], (0, 1)),
    ],
)
def test_docstring_examples(values, expected):
    assert total_and_multiple(values) == expected


def test_returns_tuple_of_two_ints():
    result = total_and_multiple([1, 2, 3])
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(x, int) for x in result)


def test_does_not_mutate_input():
    values = [3, 1, 2]
    total_and_multiple(values)
    assert values == [3, 1, 2]
