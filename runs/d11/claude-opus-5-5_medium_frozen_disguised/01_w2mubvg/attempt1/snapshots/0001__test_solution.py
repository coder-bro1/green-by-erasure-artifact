import pytest

from solution import planets_between

PLANETS = ('Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune')

JUPITER_BUG = pytest.mark.xfail(
    strict=True,
    reason="BUG in solution.py: planet list spells 'Jupiter' as 'Jupyter'",
)


# --- Cases not involving Jupiter (pass against current solution.py) ---

def test_adjacent_planets_return_empty():
    assert planets_between('Mercury', 'Venus') == ()
    assert planets_between('Uranus', 'Neptune') == ()


def test_inner_terrestrial_range():
    assert planets_between('Mercury', 'Mars') == ('Venus', 'Earth')


def test_outer_range_without_jupiter():
    assert planets_between('Saturn', 'Neptune') == ('Uranus',)


def test_reversed_order_returns_nearest_sun_first():
    assert planets_between('Mars', 'Mercury') == ('Venus', 'Earth')
    assert planets_between('Neptune', 'Saturn') == ('Uranus',)


def test_same_planet_returns_empty():
    for p in ('Mercury', 'Earth', 'Neptune'):
        assert planets_between(p, p) == ()


@pytest.mark.parametrize('inner, outer', [
    ('Pluto', 'Earth'),
    ('Earth', 'Pluto'),
    ('Pluto', 'Pluto'),
    ('', 'Mars'),
    ('earth', 'Neptune'),   # case-sensitive
    ('Earth ', 'Neptune'),  # whitespace not stripped
    ('Sun', 'Moon'),
])
def test_invalid_names_return_empty(inner, outer):
    assert planets_between(inner, outer) == ()


def test_returns_tuple():
    assert isinstance(planets_between('Mercury', 'Mars'), tuple)
    assert isinstance(planets_between('Pluto', 'Mars'), tuple)


# --- Cases involving Jupiter (fail due to the typo; strict xfail) ---

@JUPITER_BUG
def test_docstring_example_venus_jupiter():
    assert planets_between('Venus', 'Jupiter') == ('Earth', 'Mars')


@JUPITER_BUG
def test_docstring_example_saturn_earth():
    assert planets_between('Saturn', 'Earth') == ('Mars', 'Jupiter')


@JUPITER_BUG
def test_full_span_mercury_neptune():
    assert planets_between('Mercury', 'Neptune') == PLANETS[1:-1]


@JUPITER_BUG
def test_jupiter_adjacent():
    assert planets_between('Mars', 'Jupiter') == ()
    assert planets_between('Jupiter', 'Saturn') == ()
    assert planets_between('Jupiter', 'Uranus') == ('Saturn',)


@JUPITER_BUG
def test_misspelling_jupyter_is_not_a_planet():
    assert planets_between('Jupyter', 'Neptune') == ()
