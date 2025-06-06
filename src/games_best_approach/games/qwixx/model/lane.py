"""Lane model."""
from __future__ import annotations

from enum import Enum, auto
from itertools import islice
from typing import Iterator

MINIMAL_CLOSE_SELECTIONS = 5

LANE_MIN = 2
LANE_MAX = 13

class Direction(Enum):
    """Direction of lane."""
    ASC = auto()
    DESC = auto()

    @property
    def step(self):
        """Step representation of  direction."""
        if self is Direction.ASC:
            return 1
        elif self is Direction.DESC:
            return -1
        raise ValueError('Direction must be ASC or DESC')

class Color(Enum):
    """Color of lane."""
    R = auto()
    Y = auto()
    G = auto()
    B = auto()

    @property
    def direction(self) -> Direction:
        """Direction of lane."""
        if self in {Color.R, Color.Y}:
            return Direction.ASC
        elif self in {Color.G, Color.B}:
            return Direction.DESC
        raise ValueError(f'Unknown direction for color {self}')

    @property
    def asc(self) -> bool:
        """If color has ascending direction."""
        if self.direction is Direction.ASC:
            return True
        elif self.direction is Direction.DESC:
            return False
        raise ValueError('Direction must be ASC or DESC')

class Lane:
    """Model representing a lane."""

    def __init__(self, color: Color):
        """Initialize lane."""
        self.color = color
        if self.asc:
            self._lane = list(range(LANE_MIN, LANE_MAX + 1, color.direction.step))
        else:
            self._lane = list(range(LANE_MAX - 1, LANE_MIN - 1 - 1, color.direction.step))

    def __str__(self):
        """String variant of lane."""
        lane = ' | '.join('><' if n is None else f'{n:02d}' for n in self._lane)
        return f'{self.color.name} ( {lane} )'

    @property
    def asc(self) -> bool:
        """If lane has ascending direction."""
        return self.color.asc

    @property
    def possible(self) -> list[int]:
        """possible lane numbers."""
        reversed_lane = self._lane[::-1]

        if None not in self._lane:
            if not self.can_close:
                return reversed_lane[1:]
            return reversed_lane

        possible_numbers = list(islice(reversed_lane, reversed_lane.index(None)))[1:]  # closing bonus not selectable

        if any(p is None for p in possible_numbers):
            raise ValueError('possible lane numbers cannot be None')

        return possible_numbers

    @property
    def can_close(self) -> bool:
        """If lane can be closed."""
        return self._lane.count(None) >= MINIMAL_CLOSE_SELECTIONS

    def select(self, number: int) -> Lane:
        """Select number in lane."""
        if number not in self.possible:
            raise ValueError(f'number {number} not in possible options: {self.possible}')

        if self.asc:
            internal_index = number - LANE_MIN
        else:
            internal_index = LANE_MAX - number - 1

        last_possible = self.possible[0]

        if self.can_close and number == last_possible:
            self._lane[-1] = None

        self._lane[internal_index] = None

        return self

if __name__ == '__main__':
    l = Lane(Color.B).select(12).select(11).select(10).select(9).select(8)
    print(l.select(2))
    print(Lane(Color.R).select(2).select(3).select(4).select(5).select(6).select(12))