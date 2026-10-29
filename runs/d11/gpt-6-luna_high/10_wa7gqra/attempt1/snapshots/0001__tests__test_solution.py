import pytest

from solution import bf


@pytest.mark.parametrize(
    ("planet1", "planet2", "expected"),
    [
        ("Jupiter", "Neptune", ("Saturn", "Uranus")),
        ("Earth", "Mercury", ("Venus",)),
        ("Mercury", "Uranus", ("Venus", "Earth", "Mars", "Jupiter", "Saturn")),
        # Results are ordered by distance from the Sun, regardless of input order.
        ("Neptune", "Jupiter", ("Saturn", "Uranus")),
        ("Venus", "Earth", ()),
        ("Mercury", "Neptune", ("Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus")),
        ("Mercury", "Mercury", ()),
    ],
)
def test_bf_returns_planets_strictly_between_inputs_in_solar_order(
    planet1, planet2, expected
):
    assert bf(planet1, planet2) == expected


@pytest.mark.parametrize(
    ("planet1", "planet2"),
    [
        ("Pluto", "Earth"),
        ("Earth", "pluto"),
        ("", "Mars"),
        ("Earth ", "Mars"),
    ],
)
def test_bf_returns_empty_tuple_when_a_planet_name_is_invalid(planet1, planet2):
    assert bf(planet1, planet2) == ()
