"""
Qwuixx game instance.

1. roll dice
2. active player choose numbers
    a. use white first and then color
    b. use only color
    c. don't want to take a number -> miss
    d. can't take a number -> miss
3. other players decide if they want to use white

4. if one player closed a lane, others can do the same instead of other actions
5. if 4 misses used -> game end
6. if 2 lanes closed -> game end
7. evaluate boards (print leader board)

"""

from games_best_approach.games.qwixx.model.board import Board
from games_best_approach.games.qwixx.model.dice import Dice
from games_best_approach.games.qwixx.model.lane import Color, LANE_MAX, LANE_MIN

MIN_PLAYER = 2
MAX_PLAYER = 4

GAME_END_LANES_CLOSED = 2


class Qwuixx:

    def __init__(self, player: int):
        """Initialize Qwuixx."""
        if not (MIN_PLAYER <= player <= MAX_PLAYER):
            raise ValueError(f'player must be between {MIN_PLAYER} and {MAX_PLAYER}')
        self.boards = {p: Board() for p in range(1, player + 1)}
        self._active_player = 1
        self.dice = Dice()

    def _current_board(self, player: int = 0) -> Board:
        """Get board for current player."""
        current_player = player or self._active_player
        return self.boards[current_player]

    @property
    def _other_player(self) -> list[int]:
        """Other player then current player."""
        next_player = self._next_player()
        other_player = []
        while next_player != self._active_player:
            other_player.append(next_player)
            next_player = self._next_player(next_player)

        return other_player

    def play(self):
        """Play Qwuixx game."""
        while self._is_not_finished():
            self.dice.roll()
            dice_per_player = {}
            # play active player
            if self._is_dice_possible():
                print(self.dice)
                self._print_current_player()
                dice_per_player[self._active_player] = self._get_valid_selection()
            else:
                print(f"No dice options for player {self._active_player}, that's a miss.")
                self._current_board().skip()

            # play other players
            for player in self._other_player:
                if self._is_dice_possible():
                    print(self.dice)
                    self._print_current_player(player)
                    dice_per_player[player] = self._get_valid_selection(player)
                else:
                    print(f'No dice options for player {player}')

            # if white can close lane, check if anyone does
            self._care_for_closing(dice_per_player)

            self._active_player = self._next_player()

        # evaluate boards
        scores = [(player, board.score) for player, board in self.boards.items()]
        scores.sort(key=lambda x: x[1])
        for player, score in scores:
            print(f'Player {player}: {score}')

    def _care_for_closing(self, dice_per_player: dict[int, list[tuple[Color, int]]]) -> None:
        """Care for closing if applicable."""
        if self._is_player_closing_lane(dice_per_player):
            closing_color = self._get_closing_color(dice_per_player)

            for player, dice in dice_per_player.items():
                if (closing_color, self.dice.white) in dice:
                    # player already want's to use white dice to close
                    continue
                self._request_dice_switch(player, dice, closing_color, dice_per_player)


    def _get_closing_color(self, dice_per_player: dict[int, list[tuple[Color, int]]]) -> Color:
        """Get closing color of closing player."""
        closing_color = None
        for player, dice in dice_per_player.items():
            for c, n in dice:
                if (
                    n == self.dice.white
                    and self._current_board(player).would_close([(c, n)])
                ):
                    closing_color = c
                    
        if closing_color is None:
            raise ValueError('Impossible state: no closing color found')
        
        return closing_color

    def _is_player_closing_lane(self, dice_per_player: dict[int, list[tuple[Color, int]]]) -> bool:
        """Check if one player is closing lane with white dice."""
        return (
            (
                self.dice.white == LANE_MIN
                or self.dice.white == LANE_MAX
            )
            and any(
                self._current_board(player).would_close(
                    [(c, n) for c, n in dice if n == self.dice.white]
                )
                for player, dice in dice_per_player.items()
            )
        )

    def _get_valid_selection(self, player: int = 0) -> list[tuple[Color, int]]:
        """Get valid selection."""
        while True:
            chosen_dice = self.dice.get_chosen(only_white=bool(player))
            if not chosen_dice and bool(player):
                return chosen_dice
            valid_selection = self._current_board(player).is_select_possible(chosen_dice)
            if valid_selection:
                return chosen_dice
            print('Selection can not applied to board, try again.')

    def _next_player(self, player: int = 0) -> int:
        """Get next player."""
        current_player = player or self._active_player
        return current_player % len(self.boards) + 1

    def _would_close(self, dice: list[tuple[Color, int]], player: int = 0) -> bool:
        """Check if dice would close board of player."""
        return self._current_board(player).would_close(dice)

    def _is_dice_possible(self, player: int = 0) -> bool:
        """Check if dice is possible for current player."""
        return self._current_board(player).is_dice_possible(self.dice.options)

    def _print_current_player(self, player: int = 0) -> None:
        """Print current player and board."""
        current_player = player or self._active_player
        print(f'Player: {current_player}')
        print(self._current_board(player))

    def _request_dice_switch(
        self,
        player: int,
        dice: list[tuple[Color, int]],
        closing_color: Color,
        dice_per_player: dict[int, list[tuple[Color, int]]],
    ) -> None:
        """Request dice switch."""
        while True:
            switch = input(
                f'Player {player}: Do you want to switch to the white dice? Current selection: {dice}[Y]/N')
            if switch == 'Y':
                if player == self._active_player:
                    new_dice = (
                            [(c, n) for c, n in dice if n != self.dice.white]
                            + [(closing_color, self.dice.white)]
                    )
                else:
                    new_dice = [(closing_color, self.dice.white)]
                dice_per_player[player] = new_dice
                return
            elif switch == 'N':
                return
            else:
                print(f'Invalid input: {switch} Try again.')

    def _is_not_finished(self) -> bool:
        """Check if no one finished."""
        closed_colors = []
        for player, board in self.boards:
            if board.closed_by_skips:
                return True
            closed_colors += board.closed_colors

        if len(set(closed_colors)) >= GAME_END_LANES_CLOSED:
            return True

        return False



if __name__ == '__main__':
    Qwuixx(MIN_PLAYER).play()