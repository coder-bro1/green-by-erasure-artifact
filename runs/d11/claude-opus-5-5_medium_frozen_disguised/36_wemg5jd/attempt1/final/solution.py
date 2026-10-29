def most_frequent_letters(text):
    """text holds lowercase letters separated by spaces. Return a dictionary that maps each letter occurring most often to its number of occurrences; all letters tied for the maximum are included. An empty string gives an empty dictionary.

    >>> most_frequent_letters('p q p')
    {'p': 2}
    >>> most_frequent_letters('z y')
    {'z': 1, 'y': 1}
    >>> most_frequent_letters('')
    {}
    """
    counts = {}
    parts = text.split(' ')
    best = 1
    for item in parts:
        if parts.count(item) > best and item != '':
            best = parts.count(item)
    if best > 0:
        for item in parts:
            if parts.count(item) == best:
                counts[item] = best
    return counts
