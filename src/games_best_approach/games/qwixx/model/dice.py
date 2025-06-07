"""
Dice model.

This represents 6 dice. 2 are white and the others are red, yellow, blue and green
"""
from random import randint

from games_best_approach.games.qwixx.model.lane import Color


class Dice:

    options = dict[Color, list[int]]()
    white = 0
    w1 = 0
    w2 = 0
    r = 0
    y = 0
    b = 0
    g = 0

    def roll(self) -> None:
        """Roll dice and set options for colors."""
        self.w1 = randint(1, 6)
        self.w2 = randint(1, 6)
        self.r = randint(1, 6)
        self.y = randint(1, 6)
        self.b = randint(1, 6)
        self.g = randint(1, 6)

        color_dice = {
            Color.R: self.r,
            Color.Y: self.y,
            Color.B: self.b,
            Color.G: self.g,
        }

        self.white = self.w1 + self.w2
        for color, die in color_dice.items():
            self.options[color] = [
                die + self.w1,
                self.w2 + die,
            ]

    def __str__(self):
        """String variant of dice."""
        if not self.white:
            raise ValueError('Dice must rolled at least once.')

        colors = '\t'.join(['w', 'w', 'r', 'y', 'b', 'g'])
        numbers = '\t'.join(
            f'{n:02d}' for n in [self.w1, self.w2, self.r, self.y, self.b, self.g]
        )

        return f'{colors}\n{numbers}'


if __name__ == '__main__':
    dice = Dice()
    dice.roll()
    print(dice)
