def is_one_direction(seq: list):
    """Return True when the elements of seq never decrease or never increase, and False otherwise.

    >>> is_one_direction([1, 1, 3])
    True
    >>> is_one_direction([5, 2, 2, 0])
    True
    >>> is_one_direction([2, 9, 4])
    False
    """
    if seq == sorted(seq) or seq == sorted(seq, reverse=True):
        return False
    return True
