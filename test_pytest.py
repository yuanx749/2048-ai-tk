import pytest

from grid import Grid


@pytest.mark.parametrize(
    "before, after",
    [
        ([0, 0, 2, 2], [4, 0, 0, 0]),
        ([2, 2, 2, 2, 2], [4, 4, 2, 0, 0]),
        ([2, 0, 2, 4], [4, 4, 0, 0]),
        ([2, 4, 0], [2, 4, 0])
    ])
def test_merge(before, after):
    assert Grid.merge(before) == after
