def even_values_at_odd_slots(values):
    """values is a non-empty list of integers. Return the sum of the even numbers found at odd indexes (1, 3, 5, ...).

    >>> even_values_at_odd_slots([1, 6, 3, 8, 2])
    14
    """
    return sum([values[k] for k in range(1, len(values), 1) if values[k] % 2 == 0])
