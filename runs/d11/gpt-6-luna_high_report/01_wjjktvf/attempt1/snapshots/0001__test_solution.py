import pytest

from solution import bf


@pytest.mark.parametrize(
    ("planet1", "planet2", "expected"),
    [
        ("Jupiter", "Neptune", ("Saturn", "Uranus")),
        ("Earth", "Mercury", ("Venus",)),
        (
            "Mercury",
            "Uranus",
            ("Venus", "Earth", "Mars", "Jupiter", "Saturn"),
        ),
        # The result is always ordered by proximity to the Sun, regardless
        # of the order in which the endpoints are supplied.
        ("Neptune", "Jupiter", ("Saturn", "Uranus")),
        ("Uranus", "Mercury", ("Venus", "Earth", "Mars", "Jupiter", "Saturn")),
        # Adjacent or identical planets have no planets between them.
        ("Venus", "Earth", ()),
        ("Earth", "Earth", ()),
    ],
)
def test_planets_between(planet1, planet2, expected):
    assert bf(planet1, planet2) == expected


@pytest.mark.parametrize(
    ("planet1", "planet2"),
    [
        ("Pluto", "Earth"),
        ("Earth", "Pluto"),
        ("earth", "Mars"),
        ("Mercury ", "Mars"),
        ("", "Neptune"),
    ],
)
def test_invalid_planet_name_returns_empty_tuple(planet1, planet2):
    assert bf(planet1, planet2) == ()
