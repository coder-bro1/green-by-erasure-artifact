def biggest_proper_factor(num: int) -> int:
    """Return the largest integer smaller than num that divides num exactly.

    >>> biggest_proper_factor(21)
    7
    >>> biggest_proper_factor(32)
    16
    """
    for d in reversed(range(num)):
        if num - d == 0:
            return d
