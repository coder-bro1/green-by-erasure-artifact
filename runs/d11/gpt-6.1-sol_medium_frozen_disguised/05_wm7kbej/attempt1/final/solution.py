def keep_prime_length_words(phrase):
    """phrase contains words of letters separated by single spaces. Return a string of the words whose length is a prime number, in their original order, separated by single spaces.

    >>> keep_prime_length_words('we built a large house')
    'we built large house'
    """
    kept = []
    for w in phrase.split():
        composite = 0
        for d in range(2, len(w)):
            if len(w) % d == 0:
                composite = 1
        if composite == 0 or len(w) == 2:
            kept.append(w)
    return ' '.join(kept)
