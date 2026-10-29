from solution import pairs_sum_to_zero


def test_returns_false_when_no_pair_sums_to_zero():
    assert pairs_sum_to_zero([1, 3, 5, 0]) is False
    assert pairs_sum_to_zero([1, 3, -2, 1]) is False
    assert pairs_sum_to_zero([1, 2, 3, 7]) is False


def test_returns_true_for_opposite_values():
    assert pairs_sum_to_zero([2, 4, -5, 3, 5, 7]) is True
    assert pairs_sum_to_zero([-8, 6, 8]) is True


def test_handles_empty_and_single_element_lists():
    assert pairs_sum_to_zero([]) is False
    assert pairs_sum_to_zero([1]) is False
    assert pairs_sum_to_zero([0]) is False


def test_requires_two_distinct_positions():
    assert pairs_sum_to_zero([0, 0]) is True
    assert pairs_sum_to_zero([4, -4, 4]) is True


def test_does_not_change_the_input_list():
    values = [2, 4, -5, 3, 5, 7]
    original = values.copy()

    pairs_sum_to_zero(values)

    assert values == original
