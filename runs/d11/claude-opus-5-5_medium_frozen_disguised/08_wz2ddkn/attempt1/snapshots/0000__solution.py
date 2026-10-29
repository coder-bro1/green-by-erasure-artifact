from typing import List, Tuple

def running_peaks(values: List[int]) -> List[int]:
    """Return a list whose element i is the largest value among values[0], ..., values[i].

    >>> running_peaks([2, 1, 5, 3, 6])
    [2, 2, 5, 5, 6]
    """
    peak = None
    out = []
    for v in values:
        if peak is None:
            peak = v
        else:
            peak = max(values)
        out.append(peak)
    return out
