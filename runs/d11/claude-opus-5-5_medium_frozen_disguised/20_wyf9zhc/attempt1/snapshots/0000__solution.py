def even_length_words_sorted(words):
    """Remove the strings of odd length from words and return the remaining strings sorted by length; strings of equal length are in alphabetical order.

    >>> even_length_words_sorted(['dd', 'c', 'ab', 'eeee'])
    ['ab', 'dd', 'eeee']
    """
    words.sort()
    kept = []
    for w in words:
        if len(w) % 2 == 0:
            kept.append(w)
    return kept
