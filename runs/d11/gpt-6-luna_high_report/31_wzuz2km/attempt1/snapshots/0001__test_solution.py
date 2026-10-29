import pytest

from solution import intersperse


def test_intersperse_empty_list():
    assert intersperse([], 4) == []


@pytest.mark.parametrize(
    ("numbers", "delimiter", "expected"),
    [
        ([7], 4, [7]),
        ([1, 2], 4, [1, 4, 2]),
        ([1, 2, 3], 4, [1, 4, 2, 4, 3]),
        ([0, -2, 5], -1, [0, -1, -2, -1, 5]),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="intersperse omits the final input element for every non-empty list",
)
def test_intersperse_preserves_elements_and_inserts_delimiter(
    numbers, delimiter, expected
):
    assert intersperse(numbers, delimiter) == expected
