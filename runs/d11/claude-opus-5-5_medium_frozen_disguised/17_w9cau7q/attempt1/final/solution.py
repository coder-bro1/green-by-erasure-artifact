from typing import List

def weave_separator(values: List[int], sep: int) -> List[int]:
    """Return a new list in which sep is placed between every pair of neighbouring items of values.

    >>> weave_separator([7, 8], 0)
    [7, 0, 8]
    >>> weave_separator([5, 5, 5], -1)
    [5, -1, 5, -1, 5]
    >>> weave_separator([], 2)
    []
    """
    if not values:
        return []
    out = []
    for item in values[:-1]:
        out.append(item)
        out.append(sep)
    return out
