import pytest

from solution import bf

JUPITER_BUG = (
    "solution.py spells the fifth planet 'Jupyter' instead of 'Jupiter', so "
    "'Jupiter' is rejected as an invalid name and ranges spanning it contain 'Jupyter'"
)


# --- Cases not involving Jupiter ---------------------------------------------

def test_docstring_example_reverse_order():
    # Docstring writes ("Venus"), which is a string in Python; a 1-tuple is intended.
    assert bf("Earth", "Mercury") == ("Venus",)


def test_adjacent_planets_return_empty_tuple():
    assert bf("Mercury", "Venus") == ()
    assert bf("Uranus", "Neptune") == ()
    assert bf("Neptune", "Uranus") == ()


def test_same_planet_returns_empty_tuple():
    assert bf("Earth", "Earth") == ()


def test_inner_range():
    assert bf("Mercury", "Mars") == ("Venus", "Earth")
    assert bf("Mars", "Mercury") == ("Venus", "Earth")


def test_outer_range():
    assert bf("Saturn", "Neptune") == ("Uranus",)


@pytest.mark.parametrize(
    "p1, p2",
    [
        ("Pluto", "Earth"),
        ("Earth", "Pluto"),
        ("", "Mars"),
        ("earth", "Mars"),       # case-sensitive names
        ("Makemake", "Pluto"),
        ("Jupyter", "Earth"),    # misspelling is not a correct planet name
    ],
)
def test_invalid_names_return_empty_tuple(p1, p2):
    assert bf(p1, p2) == ()


def test_return_type_is_tuple():
    assert isinstance(bf("Mercury", "Mars"), tuple)
    assert isinstance(bf("Pluto", "Mars"), tuple)


# --- Cases involving Jupiter (fail because of the misspelling) ---------------

@pytest.mark.xfail(strict=True, reason=JUPITER_BUG)
def test_docstring_example_jupiter_neptune():
    assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")


@pytest.mark.xfail(strict=True, reason=JUPITER_BUG)
def test_docstring_example_mercury_uranus():
    assert bf("Mercury", "Uranus") == ("Venus", "Earth", "Mars", "Jupiter", "Saturn")


@pytest.mark.xfail(strict=True, reason=JUPITER_BUG)
def test_full_span_neptune_mercury():
    assert bf("Neptune", "Mercury") == (
        "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus",
    )


@pytest.mark.xfail(strict=True, reason=JUPITER_BUG)
def test_jupiter_as_endpoint_reverse():
    assert bf("Jupiter", "Earth") == ("Mars",)
