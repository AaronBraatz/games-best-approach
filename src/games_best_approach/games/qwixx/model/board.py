"""Model for board."""
from games_best_approach.games.qwixx.model.lane import Color, Lane


class Board:

    def __init__(self):
        """Initialize board."""
        self.lanes = {color: Lane(color) for color in Color}

    def __str__(self):
        """String variant of Board."""
        return '\n'.join(str(l) for l in self.lanes.values())

if __name__ == '__main__':
    print(Board())