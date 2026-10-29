import pytest

from solution import tri


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, [1]),
        (1, [1, 3]),
        (2, [1, 3, 2]),
        (3, [1, 3, 2, 8]),
        (4, [1, 3, 2, 8, 3]),
        (8, [1, 3, 2, 8, 3, 15, 4, 24, 5]),
    ],
)
def test_tri_returns_first_n_plus_one_values(n, expected):
    result = tri(n)

    assert isinstance(result, list)
    assert result == expected
    assert len(result) == n + 1


def test_tri_values_follow_documented_recurrence():
    values = tri(10)

    for n in range(2, len(values)):
        if n % 2 == 0:
            assert values[n] == 1 + n / 2
        else:
            assert values[n] == values[n - 1] + values[n - 2] + (n + 3) / 2
