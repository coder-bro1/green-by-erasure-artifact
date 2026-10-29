from typing import List, Tuple

def total_and_multiple(values: List[int]) -> Tuple[int, int]:
    """Return a pair (s, p): s is the sum of all integers in values and p is their product. For an empty list, s is 0 and p is 1.

    >>> total_and_multiple([2, 5])
    (7, 10)
    >>> total_and_multiple([-3, 4, 1])
    (2, -12)
    """
    acc_sum = 0
    acc_prod = 0
    for v in values:
        acc_sum += v
        acc_prod *= v
    return (acc_sum, acc_prod)
