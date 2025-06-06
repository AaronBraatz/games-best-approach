"""Test lane model."""

import pytest

from games_best_approach.games.qwixx.model.lane import Direction, Color, Lane

ASC_LANE = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
DESC_LANE = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]


@pytest.mark.parametrize(
    'direction, step',
    [
        (Direction.DESC, -1),
        (Direction.ASC, 1),

    ]
)
def test_direction_step(direction: Direction, step: int):
    """Test direction enum step."""
    assert direction.step == step


@pytest.mark.parametrize(
    'color, direction, asc',
    [
        (Color.R, Direction.ASC, True),
        (Color.Y, Direction.ASC, True),
        (Color.B, Direction.DESC, False),
        (Color.G, Direction.DESC, False),
    ]
)
def test_color_direction_asc(color: Color, direction: Direction, asc: bool):
    """Test color enum."""
    assert color.direction == direction
    assert color.asc == asc

@pytest.mark.parametrize(
    'lane, numbers, asc',
    [
        (Lane(Color.R), ASC_LANE, True),
        (Lane(Color.Y), ASC_LANE, True),
        (Lane(Color.B), DESC_LANE, False),
        (Lane(Color.G), DESC_LANE, False),
    ]
)
def test_lane_model(lane: Lane, numbers: list[int], asc: bool):
    """Test lane model."""
    assert lane._lane == numbers
    assert lane.asc == asc


def test_lane_select():
    """Test lane select."""

    asc_lane = Lane(Color.R).select(2)
    assert (
       asc_lane
    )._lane == [None, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    asc_lane = (
        asc_lane
        .select(5)
        .select(7)
        .select(9)
        .select(11)
    )
    assert (
       asc_lane
    )._lane == [None, 3, 4, None, 6, None, 8, None, 10, None, 12, 13]
    asc_lane = asc_lane.select(12)
    assert (
       asc_lane
    )._lane == [None, 3, 4, None, 6, None, 8, None, 10, None, None, None]

    desc_lane = Lane(Color.B).select(12)
    assert (
           desc_lane
    )._lane == [None, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    desc_lane = (
        desc_lane
        .select(10)
        .select(8)
        .select(6)
        .select(4)
    )
    assert (
           desc_lane
    )._lane == [None, 11, None, 9, None, 7, None, 5, None, 3, 2, 1]
    desc_lane = desc_lane.select(2)
    assert (
           desc_lane
    )._lane == [None, 11, None, 9, None, 7, None, 5, None, 3, None, None]

@pytest.mark.parametrize(
    'lane, possible',
    [
        (Lane(Color.R).select(10), [12, 11]),
        (Lane(Color.B).select(7), [2, 3, 4, 5, 6]),
    ]
)
def test_lane_possible(lane: Lane, possible: list[int]):
    """Test lane possible numbers."""
    assert lane.possible == possible

@pytest.mark.parametrize(
    'lane, can_close',
    [
        (Lane(Color.R).select(10), False),
        (Lane(Color.R).select(10).select(11), False),
        (Lane(Color.R).select(9).select(10).select(11), False),
        (Lane(Color.R).select(9).select(10).select(11).select(12), False),
        (Lane(Color.R).select(8).select(9).select(10).select(11).select(12), True),
        (Lane(Color.R).select(7).select(8).select(9).select(10).select(11).select(12), True),
    ]
)
def test_lane_can_close(lane: Lane, can_close: bool):
    """Test lane can close."""
    assert lane.can_close == can_close

def test_lane_str():
    """Test lane str."""
    assert str(
        Lane(Color.R)
    ) == 'R ( 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 )'
    assert str(
        Lane(Color.R).select(2).select(12)
    ) == 'R ( >< | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | >< | 13 )'
    assert str(
        Lane(Color.R).select(2).select(3).select(4).select(5).select(6).select(12)
    ) == 'R ( >< | >< | >< | >< | >< | 07 | 08 | 09 | 10 | 11 | >< | >< )'
    assert str(
        Lane(Color.G)
    ) == 'G ( 12 | 11 | 10 | 09 | 08 | 07 | 06 | 05 | 04 | 03 | 02 | 01 )'
    assert str(
        Lane(Color.G).select(12).select(2)
    ) == 'G ( >< | 11 | 10 | 09 | 08 | 07 | 06 | 05 | 04 | 03 | >< | 01 )'
    assert str(
        Lane(Color.G).select(12).select(11).select(10).select(9).select(8).select(2)
    ) == 'G ( >< | >< | >< | >< | >< | 07 | 06 | 05 | 04 | 03 | >< | >< )'

def test_lane_select_not_possible():
    """Test lane select not possible."""
    with pytest.raises(
        ValueError,
        match=r'number 3 not in possible options: \[12\]'
    ):
        Lane(Color.R).select(11).select(3)
    with pytest.raises(
        ValueError,
        match=r'number 10 not in possible options: \[2\]'
    ):
        Lane(Color.B).select(3).select(10)