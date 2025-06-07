"""Test board model."""
import pytest

from games_best_approach.games.qwixx.model.board import Board
from games_best_approach.games.qwixx.model.lane import Color
from tests.test_games.test_qwuixx.test_model.test_lane import ASC_LANE, DESC_LANE

BOARD_STR = (
    'R ( 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 )\n'
    'Y ( 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 )\n'
    'G ( 12 | 11 | 10 | 09 | 08 | 07 | 06 | 05 | 04 | 03 | 02 | 01 )\n'
    'B ( 12 | 11 | 10 | 09 | 08 | 07 | 06 | 05 | 04 | 03 | 02 | 01 )'
)
BOARD_WITH_SELECTIONS_STR = (
    'R ( >< | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | >< | 13 )\n'
    'Y ( 02 | 03 | 04 | 05 | 06 | >< | 08 | 09 | 10 | 11 | 12 | 13 )\n'
    'G ( 12 | 11 | 10 | 09 | 08 | 07 | 06 | 05 | 04 | >< | 02 | 01 )\n'
    'B ( >< | 11 | 10 | 09 | 08 | 07 | 06 | 05 | 04 | >< | 02 | 01 )'
)


@pytest.fixture
def board() -> Board:
    return Board()


def test_board_init(board):
    """Test board model init."""
    assert board.lanes[Color.R]._lane == ASC_LANE
    assert board.lanes[Color.Y]._lane == ASC_LANE
    assert board.lanes[Color.B]._lane == DESC_LANE
    assert board.lanes[Color.G]._lane == DESC_LANE

def test_board_select_number(board):
    """Test board select number."""
    board.select(Color.R, 2)
    assert board.lanes[Color.R]._lane == [None] + ASC_LANE[1:]
    assert board.lanes[Color.Y]._lane == ASC_LANE
    assert board.lanes[Color.B]._lane == DESC_LANE
    assert board.lanes[Color.G]._lane == DESC_LANE

    board.select(Color.B, 12)
    assert board.lanes[Color.R]._lane == [None] + ASC_LANE[1:]
    assert board.lanes[Color.Y]._lane == ASC_LANE
    assert board.lanes[Color.B]._lane == [None] + DESC_LANE[1:]
    assert board.lanes[Color.G]._lane == DESC_LANE

    board.select(Color.R, 12)
    assert board.lanes[Color.R]._lane == [None] + ASC_LANE[1:-2] + [None, 13]
    assert board.lanes[Color.Y]._lane == ASC_LANE
    assert board.lanes[Color.B]._lane == [None] + DESC_LANE[1:]
    assert board.lanes[Color.G]._lane == DESC_LANE

    board.select(Color.B, 2)
    assert board.lanes[Color.R]._lane == [None] + ASC_LANE[1:-2] + [None, 13]
    assert board.lanes[Color.Y]._lane == ASC_LANE
    assert board.lanes[Color.B]._lane == [None] + DESC_LANE[1:-2] + [None, 1]
    assert board.lanes[Color.G]._lane == DESC_LANE


def test_board_possible(board):
    """Test board model possible."""
    board.select(Color.R, 2)
    assert board.possible[Color.R] == DESC_LANE[:-2]
    assert board.possible[Color.Y] == DESC_LANE[:-1]

    board.select(Color.B, 12)
    assert board.possible[Color.B] == ASC_LANE[:-2]
    assert board.possible[Color.G] == ASC_LANE[:-1]

    board.select(Color.R, 11)
    assert board.possible[Color.R] == [12]
    assert board.possible[Color.Y] == DESC_LANE[:-1]

    board.select(Color.B, 3)
    assert board.possible[Color.B] == [2]
    assert board.possible[Color.G] == ASC_LANE[:-1]

def test_board_str(board):
    """Test board model str."""
    assert str(board) == BOARD_STR

    board.select(Color.R, 2)
    board.select(Color.B, 12)
    board.select(Color.R, 12)
    board.select(Color.B, 3)
    board.select(Color.G, 3)
    board.select(Color.Y, 7)

    assert str(board) == BOARD_WITH_SELECTIONS_STR