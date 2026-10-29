def count_vowel_sounds(word):
    """Return how many vowels word contains. The vowels are a, e, i, o and u in either case; the letter y (or Y) also counts, but only when it is the last character of word.

    >>> count_vowel_sounds('sky')
    1
    >>> count_vowel_sounds('Queue')
    4
    >>> count_vowel_sounds('Banana')
    3
    """
    letters = 'aeiouyAEIOUY'
    total = sum((ch in letters for ch in word))
    return total
