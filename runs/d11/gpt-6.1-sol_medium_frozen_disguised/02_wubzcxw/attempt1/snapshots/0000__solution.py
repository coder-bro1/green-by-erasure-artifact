def fewer_letters(first, second):
    """Count the characters in all strings of first and in all strings of second. Return the list with the smaller total; when both totals are equal, return first.

    >>> fewer_letters(['ab', 'c'], ['xyz', 'w'])
    ['ab', 'c']
    >>> fewer_letters(['long'], ['a', 'b'])
    ['a', 'b']
    >>> fewer_letters([], [])
    []
    """
    n1 = 0
    for w in first:
        n1 += len(w)
    n2 = 0
    for w in second:
        n2 += len(w)
    if n1 <= n2:
        return second
    else:
        return first
