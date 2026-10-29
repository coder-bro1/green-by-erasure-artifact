import pytest

from solution import tri


def reference_tri(n):
    """Independent implementation straight from the docstring recurrence."""

    def t(k):
        if k == 0:
            return 1  # first element, as shown in the docstring example
        if k == 1:
            return 3
        if k % 2 == 0:
            return 1 + k / 2
        return t(k - 1) + t(k - 2) + t(k + 1)

    return [t(k) for k in range(n + 1)]


def test_docstring_example():
    assert tri(3) == [1, 3, 2, 8]


def test_zero():
    assert tri(0) == [1]


def test_one():
    assert tri(1) == [1, 3]


def test_two():
    assert tri(2) == [1, 3, 2]


def test_docstring_values():
    seq = tri(4)
    assert seq[1] == 3
    assert seq[2] == 2
    assert seq[3] == 8
    assert seq[4] == 3


@pytest.mark.parametrize(
    "n, expected",
    [
        (4, [1, 3, 2, 8, 3]),
        (5, [1, 3, 2, 8, 3, 15]),
        (6, [1, 3, 2, 8, 3, 15, 4]),
        (7, [1, 3, 2, 8, 3, 15, 4, 24]),
        (8, [1, 3, 2, 8, 3, 15, 4, 24, 5]),
        (9, [1, 3, 2, 8, 3, 15, 4, 24, 5, 35]),
    ],
)
def test_known_sequences(n, expected):
    assert tri(n) == expected


@pytest.mark.parametrize("n", range(0, 30))
def test_length(n):
    assert len(tri(n)) == n + 1


@pytest.mark.parametrize("n", range(0, 25))
def test_matches_reference(n):
    assert tri(n) == reference_tri(n)


def test_even_terms_formula():
    seq = tri(20)
    for k in range(2, 21, 2):
        assert seq[k] == 1 + k / 2


def test_odd_terms_recurrence():
    # Odd term k needs tri(k + 1), so compute one extra element.
    seq = tri(21)
    for k in range(3, 21, 2):
        assert seq[k] == seq[k - 1] + seq[k - 2] + seq[k + 1]


def test_prefix_consistency():
    big = tri(15)
    for n in range(16):
        assert tri(n) == big[: n + 1]


def test_all_values_are_whole_numbers():
    for value in tri(30):
        assert value == int(value)


def test_returns_list():
    assert isinstance(tri(5), list)
