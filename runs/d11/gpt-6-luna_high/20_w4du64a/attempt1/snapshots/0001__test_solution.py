import pytest

from solution import tri


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, [1]),
        (1, [1, 3]),
        (2, [1, 3, 2]),
        (3, [1, 3, 2, 8]),
        (10, [1, 3, 2, 8, 3, 15, 4, 24, 5, 35, 6]),
    ],
)
def test_tri_returns_first_n_plus_one_terms(n, expected):
    assert tri(n) == expected


def test_tri_terms_are_integers():
    assert all(type(term) is int for term in tri(10))


def test_tri_result_is_a_fresh_list():
    first = tri(3)
    second = tri(3)

    assert first == second
    assert first is not second
