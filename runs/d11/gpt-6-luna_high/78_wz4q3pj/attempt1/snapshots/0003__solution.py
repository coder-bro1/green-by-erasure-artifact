
from math import isqrt


def largest_divisor(n: int) -> int:
    """Return the largest positive divisor of ``n`` that is smaller than ``n``.

    For ``n == 1``, there is no positive proper divisor, so return 0.

    >>> largest_divisor(15)
    5
    """
    if n <= 1:
        return 0

    # The largest proper divisor is n divided by its smallest factor greater
    # than one. If no factor is found, n is prime and its largest proper
    # divisor is 1.
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            return n // i
    return 1
