"""Model for board."""
from games_best_approach.games.qwixx.model.lane import Color, Lane

_MAX_SKIPS = 4

class Board:

    def __init__(self):
        """Initialize board."""
        self._lanes = {color: Lane(color) for color in Color}
        self._skips = 0

    def __str__(self):
        """String variant of board."""
        return '\n'.join(str(l) for l in self._lanes.values())

    @property
    def closed_colors(self) -> list[Color]:
        """Colors of closed lanes."""
        return [c for c, l in self._lanes.items() if l.is_closed]

    @property
    def closed_by_skips(self) -> bool:
        """True if too many skips."""
        return self._skips >= _MAX_SKIPS

    @property
    def possible(self) -> dict[Color, list[int]]:
        """Possible lane numbers per color."""
        return {c: l.possible for c, l in self._lanes.items()}

    def select(self, color: Color, number: int) -> None:
        """Select number on lane."""
        self._lanes[color].select(number)

    def skip(self) -> None:
        """Skip dice roll."""
        if self.closed_by_skips:
            raise RuntimeError('Too many skips')

        self._skips += 1

    def would_close(self, dice: list[tuple[Color, int]]) -> bool:
        """True if a select would close lane."""
        if all(dice[0][0] == d[0] for d in dice):
            # all colors are same
            numbers = [n for _, n in dice]
            return self._lanes[dice[0][0]].would_close(numbers)

        # all different colors are possible
        return all(self._lanes[c].would_close([n]) for c, n in dice)

    def is_select_possible(self, dice: list[tuple[Color, int]]) -> bool:
        """Check if select with dice is possible."""
        if all(dice[0][0] == d[0] for d in dice):
            # all colors are same
            numbers = [n for _, n in dice]
            return self._lanes[dice[0][0]].is_select_possible(numbers)

        # all different colors are possible
        return all(self._lanes[c].is_select_possible([n]) for c, n in dice)

    def is_dice_possible(self, options: dict[Color, list[int]]) -> bool:
        """Check if select with dice is possible."""
        for color, numbers in options.items():
            for number in numbers:
                if self._lanes[color].is_select_possible([number]):
                    return True

        return False

    @property
    def score(self) -> int:
        """Score of board."""
        return sum(lane.score for lane in self._lanes.values()) - (self._skips * 5)

if __name__ == '__main__':
    print(Board())