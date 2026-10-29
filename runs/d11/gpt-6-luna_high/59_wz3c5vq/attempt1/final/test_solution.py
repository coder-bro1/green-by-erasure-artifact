from solution import rolling_max


def test_rolling_max_matches_documented_example():
    assert rolling_max([1, 2, 3, 2, 3, 4, 2]) == [1, 2, 3, 3, 3, 4, 4]


def test_rolling_max_tracks_maximum_so_far_for_negative_values():
    assert rolling_max([-4, -7, -2, -5, -8]) == [-4, -4, -2, -2, -2]


def test_rolling_max_returns_empty_list_for_empty_input():
    assert rolling_max([]) == []


def test_rolling_max_handles_single_item():
    assert rolling_max([5]) == [5]
