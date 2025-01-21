import pytest

@pytest.mark.parametrize("input,expected", [
    (2, 4),  # 2 squared should be 4
    (3, 9),  # 3 squared should be 9
    (4, 16), # 4 squared should be 16
])
def test_square(input, expected):
    assert input ** 2 == expected