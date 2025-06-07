"""
Dice model.

This represents 6 dice. 2 are white and the others are red, yellow, blue and green
"""
import re
from random import randint

from games_best_approach.games.qwixx.model.lane import Color

_DOUBLE_WHITE_MARKER = 'ww'

_CHOSEN_DICE_VALIDATION = r'^(wwr|wwy|wwb|wwg|w1b|w2b|w1g|w2g|w1r|w2r|w1y|w2y)$'


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

        colors = '\t'.join(['w1', 'w2', 'r', 'y', 'b', 'g'])
        numbers = '\t'.join(
            f'{n:02d}' for n in [self.w1, self.w2, self.r, self.y, self.b, self.g]
        )

        return f'{colors}\n{numbers}'

    @staticmethod
    def _input_chosen(_white_chosen: bool, only_white: bool = False) -> str:
        """Input loop to get chosen die string"""
        while True:
            chosen_die_input = input('Choose dice (wwb, w1b, w2b, ...), empty for skip')
            if not chosen_die_input:
                return ''

            match = re.match(_CHOSEN_DICE_VALIDATION, chosen_die_input)
            if not match:
                print(f'invalid choice: "{chosen_die_input}"')
                continue

            chosen_die = match.group(0)
            if _white_chosen and _DOUBLE_WHITE_MARKER in chosen_die:
                print('White dice cannot be chosen, choose color die or skip')
                continue

            if only_white and _DOUBLE_WHITE_MARKER not in chosen_die:
                print('Only white dice can be chosen, otherwise skip')
                continue


            if not isinstance(chosen_die, str):
                raise TypeError('chosen_die must be of type str')

            return chosen_die

    def get_chosen(self, _white_chosen: bool = False, only_white: bool = False) -> list[tuple[Color, int]]:
        """Get chosen dice."""
        chosen_die = self._input_chosen(_white_chosen)
        if not chosen_die:
            return []

        color = self._interpret_color(chosen_die)
        number = self._interpret_number(chosen_die)
        chosen_dice = [(color, number)]

        if _DOUBLE_WHITE_MARKER in chosen_die and not only_white:
            if _white_chosen:
                raise ValueError('Impossible state: white dice were chosen before')
            chosen_dice += self.get_chosen(_white_chosen=True)

        return chosen_dice

    @staticmethod
    def _interpret_color(chosen_die: str) -> Color:
        """Convert chosen die string to color"""
        return Color[chosen_die[-1].upper()]

    def _interpret_number(self, chosen_die: str, ) -> int:
        """Convert chosen die string to number."""
        color = chosen_die[-1]
        white = chosen_die[:-1]

        if white == _DOUBLE_WHITE_MARKER:
            return self.white

        return getattr(self, color) + getattr(self, white)



if __name__ == '__main__':
    dice = Dice()
    dice.roll()
    print(dice)
    print(dice.get_chosen())
