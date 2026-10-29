def planets_between(inner, outer):
    """The planets in order of distance from the Sun are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune. Return a tuple of the planets strictly between inner and outer, nearest to the Sun first. Return an empty tuple if either name is not one of these planets or both names are the same.

    >>> planets_between('Venus', 'Jupiter')
    ('Earth', 'Mars')
    >>> planets_between('Saturn', 'Earth')
    ('Mars', 'Jupiter')
    """
    order = ('Mercury', 'Venus', 'Earth', 'Mars', 'Jupyter', 'Saturn', 'Uranus', 'Neptune')
    if inner not in order or outer not in order or inner == outer:
        return ()
    a_idx = order.index(inner)
    b_idx = order.index(outer)
    if a_idx < b_idx:
        return order[a_idx + 1:b_idx]
    else:
        return order[b_idx + 1:a_idx]
