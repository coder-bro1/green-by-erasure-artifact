def ascending_with_few_repeats(nums):
    """nums holds non-negative integers. Return True when the list is in non-decreasing order and no value appears more than twice; otherwise return False.

    >>> ascending_with_few_repeats([0, 4, 4, 9])
    True
    >>> ascending_with_few_repeats([3, 3, 3])
    False
    >>> ascending_with_few_repeats([2, 1])
    False
    >>> ascending_with_few_repeats([7])
    True
    """
    seen = dict([(k, 0) for k in nums])
    for k in nums:
        seen[k] += 1
    if all((nums[k - 1] <= nums[k] for k in range(1, len(nums)))):
        return True
    else:
        return False
