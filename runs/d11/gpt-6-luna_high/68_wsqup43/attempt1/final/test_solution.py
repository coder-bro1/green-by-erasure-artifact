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
        # Reversing the endpoints should not reverse the result.
        ("Neptune", "Jupiter", ("Saturn", "Uranus")),
        # Adjacent planets have no planets between them.
        ("Venus", "Earth", ()),
        # The first and last planets have no planets outside the solar system.
        ("Mercury", "Neptune", ("Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus")),
    ],
)
def test_bf_returns_planets_between_endpoints(planet1, planet2, expected):
    assert bf(planet1, planet2) == expected


@pytest.mark.parametrize("planet", ["Mercury", "Earth", "Neptune"])
def test_bf_same_endpoint_returns_empty_tuple(planet):
    assert bf(planet, planet) == ()


@pytest.mark.parametrize(
    ("planet1", "planet2"),
    [
        ("Pluto", "Earth"),
        ("Earth", "Pluto"),
        ("earth", "Mars"),
        ("", "Venus"),
    ],
)
def test_bf_invalid_planet_name_returns_empty_tuple(planet1, planet2):
    assert bf(planet1, planet2) == ()
