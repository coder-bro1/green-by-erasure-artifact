def words_with_consonants(sentence, count):
    """Return, in their original order, the words of sentence (split on whitespace) that contain exactly count consonants. sentence contains only letters and spaces; an empty sentence gives an empty list.

    >>> words_with_consonants('Big brown fox', 2)
    ['Big', 'fox']
    >>> words_with_consonants('', 1)
    []
    """
    found = []
    for w in sentence.split():
        total = 0
        for k in range(0, len(w)):
            if w[k].lower() in ['a', 'e', 'i', 'o', 'u']:
                total += 1
        if total == count:
            found.append(w)
    return found
