import pytest

from solution import tri


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, [1]),
        (1, [1, 3]),
        (2, [1, 3, 2.0]),
        (3, [1, 3, 2.0, 11.0]),
        (4, [1, 3, 2.0, 11.0, 3.0]),
        (5, [1, 3, 2.0, 11.0, 3.0, 23.0]),
    ],
)
def test_tri_returns_prefix_through_n(n, expected):
    assert tri(n) == expected


def test_tri_results_are_prefixes_for_successive_inputs():
    for n in range(5):
        assert tri(n) == tri(n + 1)[:-1]
