"""Model for board."""
from games_best_approach.games.qwixx.model.lane import Color, Lane


class Board:

    def __init__(self):
        """Initialize board."""
        self.lanes = {color: Lane(color) for color in Color}

    def __str__(self):
        """String variant of board."""
        return '\n'.join(str(l) for l in self.lanes.values())

    @property
    def possible(self) -> dict[Color, list[int]]:
        """Possible lane numbers per color."""
        return {c: l.possible for c, l in self.lanes.items()}

    def select(self, color: Color, number: int) -> None:
        """Select number on lane."""
        self.lanes[color].select(number)

if __name__ == '__main__':
    print(Board())