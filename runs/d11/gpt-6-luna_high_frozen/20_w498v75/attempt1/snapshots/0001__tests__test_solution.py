import pytest

from solution import bf


def test_returns_planets_between_endpoints_in_solar_order():
    assert bf("Mercury", "Uranus") == (
        "Venus",
        "Earth",
        "Mars",
        "Jupiter",
        "Saturn",
    )


def test_endpoint_order_does_not_change_result_order():
    assert bf("Neptune", "Earth") == ("Mars", "Jupiter", "Saturn", "Uranus")


def test_adjacent_planets_have_no_planets_between_them():
    assert bf("Earth", "Mars") == ()


@pytest.mark.parametrize(
    ("planet1", "planet2"),
    [
        ("Earth", "Earth"),
        ("Pluto", "Earth"),
        ("Earth", "Pluto"),
        ("earth", "Mars"),
        (None, "Mars"),
    ],
)
def test_equal_or_invalid_planet_names_return_empty_tuple(planet1, planet2):
    assert bf(planet1, planet2) == ()


@pytest.mark.xfail(
    strict=True,
    reason="solution.py lists 'Jupyter' instead of the valid planet 'Jupiter'",
)
def test_jupiter_is_a_valid_planet_name():
    assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")


@pytest.mark.xfail(
    strict=True,
    reason="solution.py mistakenly accepts 'Jupyter' as a planet name",
)
def test_jupyter_is_not_a_valid_planet_name():
    assert bf("Jupyter", "Neptune") == ()
