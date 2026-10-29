import pytest

from solution import is_sorted


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], True, id="empty"),
        pytest.param([5], True, id="single"),
        pytest.param([1, 2, 3, 4, 5], True, id="ascending-five"),
        pytest.param([1, 3, 2, 4, 5], False, id="middle-inversion"),
        pytest.param([1, 2, 3, 4, 5, 6], True, id="ascending-six"),
        pytest.param([1, 2, 3, 4, 5, 6, 7], True, id="ascending-seven"),
        pytest.param([1, 3, 2, 4, 5, 6, 7], False, id="long-inversion"),
        pytest.param([1, 2, 2, 3, 3, 4], True, id="multiple-pairs"),
        pytest.param([1, 2, 2, 2, 3, 4], False, id="triple-in-middle"),
        pytest.param([0, 0], True, id="zero-pair"),
        pytest.param([0, 0, 0], False, id="zero-triple"),
        pytest.param([1, 1, 1, 2], False, id="triple-at-start"),
        pytest.param([1, 2, 2, 2], False, id="triple-at-end"),
        pytest.param([7] * 10, False, id="many-identical"),
        pytest.param([2, 1], False, id="descending-pair"),
        pytest.param([3, 2, 1], False, id="descending"),
        pytest.param([2, 1, 3], False, id="first-inversion"),
        pytest.param([1, 3, 2], False, id="last-inversion"),
        pytest.param([1, 2, 1], False, id="nonadjacent-duplicate"),
        pytest.param([0, 1, 10**100], True, id="large-integer"),
    ],
)
def test_is_sorted(numbers, expected):
    original = numbers.copy()

    assert is_sorted(numbers) is expected
    assert numbers == original
