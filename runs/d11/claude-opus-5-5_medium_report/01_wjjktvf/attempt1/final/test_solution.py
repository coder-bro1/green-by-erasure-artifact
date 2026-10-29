import pytest

from solution import bf

PLANETS = ("Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune")


@pytest.mark.parametrize(
    "p1, p2, expected",
    [
        ("Jupiter", "Neptune", ("Saturn", "Uranus")),
        ("Earth", "Mercury", ("Venus",)),
        ("Mercury", "Uranus", ("Venus", "Earth", "Mars", "Jupiter", "Saturn")),
    ],
)
def test_docstring_examples(p1, p2, expected):
    assert bf(p1, p2) == expected


def test_full_range_both_orders():
    inner = PLANETS[1:-1]
    assert bf("Mercury", "Neptune") == inner
    assert bf("Neptune", "Mercury") == inner


def test_order_of_arguments_does_not_matter_and_result_sorted_by_proximity():
    for i, a in enumerate(PLANETS):
        for j, b in enumerate(PLANETS):
            expected = PLANETS[min(i, j) + 1:max(i, j)]
            assert bf(a, b) == expected
            assert bf(a, b) == bf(b, a)


def test_adjacent_planets_return_empty_tuple():
    assert bf("Earth", "Mars") == ()
    assert bf("Mars", "Earth") == ()


def test_same_planet_returns_empty_tuple():
    assert bf("Earth", "Earth") == ()


@pytest.mark.parametrize(
    "p1, p2",
    [
        ("Pluto", "Earth"),
        ("Earth", "Pluto"),
        ("Pluto", "Sun"),
        ("", "Mars"),
        ("earth", "Neptune"),   # wrong capitalisation is not a correct name
        ("Earth ", "Neptune"),  # trailing whitespace
        ("Makemake", "Jupiter"),
    ],
)
def test_invalid_names_return_empty_tuple(p1, p2):
    assert bf(p1, p2) == ()


def test_return_type_is_tuple():
    assert isinstance(bf("Mercury", "Neptune"), tuple)
    assert isinstance(bf("Earth", "Mercury"), tuple)
    assert isinstance(bf("Pluto", "Earth"), tuple)
