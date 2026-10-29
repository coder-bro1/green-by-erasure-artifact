def tri_sum_seq(k: int):
    """A sequence is defined by s(0) = 0, s(1) = 0, s(2) = 1 and s(k) = s(k - 1) + s(k - 2) + s(k - 3) for k > 2. Return s(k).

    >>> tri_sum_seq(2)
    1
    >>> tri_sum_seq(6)
    7
    >>> tri_sum_seq(9)
    44
    """
    if k == 0:
        return 0
    if k == 1:
        return 1
    if k == 2:
        return 2
    return tri_sum_seq(k - 1) + tri_sum_seq(k - 2) + tri_sum_seq(k - 3)
