"""Test dice model."""
import random

import pytest

from games_best_approach.games.qwixx.model.dice import Dice
from games_best_approach.games.qwixx.model.lane import Color

@pytest.fixture
def fixed_random():
    """Fix random."""
    random.seed(0)

def test_dice_roll(fixed_random) -> None:
    """Test dice roll."""
    dice = Dice()
    dice.roll()
    assert dice.w1 == 4
    assert dice.w2 == 4
    assert dice.r == 1
    assert dice.y == 3
    assert dice.b == 5
    assert dice.g == 4
    assert dice.white == 8

    assert len(dice.options) == 4
    for color in Color:
        assert len(dice.options[color]) == 2

def test_dice_str(fixed_random) -> None:
    """Test dice str."""
    dice = Dice()

    with pytest.raises(ValueError, match='Dice must rolled at least once\.'):
        str(dice)

    dice.roll()
    assert str(dice) == 'w1\tw2\tr\ty\tb\tg\n04\t04\t01\t03\t05\t04'