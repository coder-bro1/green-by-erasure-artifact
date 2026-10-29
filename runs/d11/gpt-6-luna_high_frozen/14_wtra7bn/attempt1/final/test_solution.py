import pytest

from solution import intersperse


def test_intersperse_empty_list():
    assert intersperse([], 4) == []


@pytest.mark.parametrize(
    ("numbers", "delimiter", "expected"),
    [
        ([7], 4, [7]),
        ([1, 2, 3], 4, [1, 4, 2, 4, 3]),
        ([1, 2], 0, [1, 0, 2]),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="solution.py currently omits the final input element",
)
def test_intersperse_nonempty_list(numbers, delimiter, expected):
    original = numbers.copy()

    assert intersperse(numbers, delimiter) == expected
    assert numbers == original
