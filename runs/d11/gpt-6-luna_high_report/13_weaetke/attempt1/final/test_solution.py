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
        (5, [1, 3, 2, 8, 3, 15]),
        (6, [1, 3, 2, 8, 3, 15, 4]),
    ],
)
def test_tri_returns_first_n_plus_one_sequence_values(n, expected):
    assert tri(n) == expected


def test_tri_result_has_n_plus_one_values():
    for n in range(20):
        assert len(tri(n)) == n + 1
