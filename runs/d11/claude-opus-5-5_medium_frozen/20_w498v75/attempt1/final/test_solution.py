import pytest

from solution import bf

ORDER = ("Mercury", "Venus", "Earth", "Mars", "Jupyter", "Saturn", "Uranus", "Neptune")


# --- Docstring examples that do not involve Jupiter ---

def test_earth_mercury_reverse_order():
    assert bf("Earth", "Mercury") == ("Venus",)


def test_mercury_uranus():
    assert bf("Mercury", "Uranus") == ("Venus", "Earth", "Mars", "Jupyter", "Saturn")


# --- General behaviour ---

def test_returns_tuple():
    assert isinstance(bf("Mercury", "Neptune"), tuple)
    assert isinstance(bf("foo", "bar"), tuple)


def test_full_span_both_directions():
    expected = ("Venus", "Earth", "Mars", "Jupyter", "Saturn", "Uranus")
    assert bf("Mercury", "Neptune") == expected
    assert bf("Neptune", "Mercury") == expected


def test_adjacent_planets_give_empty_tuple():
    assert bf("Earth", "Mars") == ()
    assert bf("Mars", "Earth") == ()
    assert bf("Uranus", "Neptune") == ()


def test_same_planet_gives_empty_tuple():
    for p in ORDER:
        assert bf(p, p) == ()


def test_symmetry_for_all_pairs():
    for a in ORDER:
        for b in ORDER:
            assert bf(a, b) == bf(b, a)


def test_all_pairs_match_slice():
    for i, a in enumerate(ORDER):
        for j, b in enumerate(ORDER):
            lo, hi = sorted((i, j))
            expected = ORDER[lo + 1:hi] if i != j else ()
            assert bf(a, b) == expected


def test_results_sorted_by_proximity_to_sun():
    result = bf("Neptune", "Venus")
    assert result == ("Earth", "Mars", "Jupyter", "Saturn", "Uranus")
    assert list(result) == sorted(result, key=ORDER.index)


# --- Invalid input ---

@pytest.mark.parametrize(
    "p1,p2",
    [
        ("Pluto", "Earth"),
        ("Earth", "Pluto"),
        ("Pluto", "Pluto"),
        ("", "Earth"),
        ("earth", "Mars"),       # case-sensitive
        ("EARTH", "MARS"),
        (" Earth", "Mars"),      # whitespace not stripped
        ("Sun", "Neptune"),
        ("Makemake", "Eris"),
    ],
)
def test_invalid_names_give_empty_tuple(p1, p2):
    assert bf(p1, p2) == ()


# --- Known bug: solution.py spells Jupiter as "Jupyter" ---

def test_jupiter_currently_rejected():
    # Records current behaviour: the correctly spelled name is not recognised.
    assert bf("Jupiter", "Neptune") == ()
    assert bf("Mercury", "Jupiter") == ()


@pytest.mark.xfail(strict=True, reason="solution.py misspells Jupiter as 'Jupyter'")
def test_docstring_jupiter_neptune():
    assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")


@pytest.mark.xfail(strict=True, reason="solution.py misspells Jupiter as 'Jupyter'")
def test_spans_include_correct_jupiter_spelling():
    assert bf("Mercury", "Uranus") == ("Venus", "Earth", "Mars", "Jupiter", "Saturn")
