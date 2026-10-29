import pytest

from solution import bf


@pytest.mark.parametrize(
    ("planet1", "planet2", "expected"),
    [
        ("Mercury", "Venus", ()),
        ("Venus", "Mercury", ()),
        ("Earth", "Mercury", ("Venus",)),
        ("Mercury", "Uranus", ("Venus", "Earth", "Mars", "Jupiter", "Saturn")),
        ("Neptune", "Jupiter", ("Saturn", "Uranus")),
        ("Earth", "Earth", ()),
    ],
)
def test_bf_returns_intermediate_planets_in_solar_order(planet1, planet2, expected):
    assert bf(planet1, planet2) == expected


@pytest.mark.parametrize("planet", ["Pluto", "jupiter", "", None])
def test_bf_returns_empty_tuple_for_invalid_planet_names(planet):
    assert bf(planet, "Earth") == ()


@pytest.mark.xfail(
    strict=True,
    reason="solution.py spells Jupiter as Jupyter in its planet list, so the documented Jupiter name is rejected.",
)
def test_bf_accepts_jupiter_as_a_planet_name():
    assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")


@pytest.mark.xfail(
    strict=True,
    reason="solution.py spells Jupiter as Jupyter in its planet list, so it returns that typo in the documented result.",
)
def test_bf_lists_jupiter_between_mercury_and_uranus():
    assert bf("Mercury", "Uranus") == (
        "Venus",
        "Earth",
        "Mars",
        "Jupiter",
        "Saturn",
    )


@pytest.mark.xfail(
    strict=True,
    reason="Jupyter is not a documented planet name, but solution.py accepts it as Jupiter.",
)
def test_bf_rejects_jupyter_as_an_invalid_planet_name():
    assert bf("Jupyter", "Neptune") == ()
