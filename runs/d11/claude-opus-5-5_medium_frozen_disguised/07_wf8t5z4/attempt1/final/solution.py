def has_opposite_pair(nums):
    """Return True when two different positions of nums hold values that add up to zero, and False otherwise.

    >>> has_opposite_pair([4, -4, 2])
    True
    >>> has_opposite_pair([0, 3])
    False
    >>> has_opposite_pair([5])
    False
    """
    for i, a in enumerate(nums):
        for j in range(i, len(nums)):
            if a + nums[j] == 0:
                return True
    return False
