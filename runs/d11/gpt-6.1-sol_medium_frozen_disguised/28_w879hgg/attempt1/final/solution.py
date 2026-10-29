def scramble_triples(text: str):
    """Split text into consecutive groups of three characters and move the first character of every full group to its end; a shorter final group is left unchanged."""
    chunks = [text[3 * k:min(3 * k + 3, len(text))] for k in range((len(text) + 2) // 3)]
    chunks = [chunk[1:] + chunk[0] if len(chunk) == 3 else chunk for chunk in chunks]
    return ''.join(chunks)

def unscramble_triples(text: str):
    """Undo scramble_triples: given a string produced by scramble_triples, return the string it was produced from.
    """
    return scramble_triples(text)
