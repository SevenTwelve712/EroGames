from typing import Union


class Game:
    def __init__(self):
        self.current_player = 'tits'
        self.field = [['' for _ in range(3)] for __ in range(3)]
        self.ended = False
        self.tits_win = 0
        self.ass_win = 0

    def step(self, added: tuple[int, int]):
        x, y = added
        self.field[x][y] = self.current_player
        if self.get_win_positions():
            self.ended = True

            # Обновим счетчик выигрышей
            if self.current_player == 'tits':
                self.tits_win += 1
            else:
                self.ass_win += 1

            return self.current_player
        elif all([all(row) for row in self.field]):
            self.ended = True
            return 'nobody'
        self.current_player = 'ass' if self.current_player == 'tits' else 'tits'
        return None

    def get_win_positions(self) -> Union[list, bool]:
        for row in range(3):
            if self.field[row][0] == self.field[row][1] == self.field[row][2] != '':
                return [(row, col) for col in range(3)]
        for col in range(3):
            if self.field[0][col] == self.field[1][col] == self.field[2][col] != '':
                return [(row, col) for row in range(3)]
        if self.field[0][0] == self.field[1][1] == self.field[2][2] != '':
            return [(0, 0), (1, 1), (2, 2)]
        if self.field[0][2] == self.field[1][1] == self.field[2][0] != '':
            return [(0, 2), (1, 1), (2, 0)]
        return False

    def new_game(self):
        self.current_player = 'tits'
        self.field = [['' for _ in range(3)] for __ in range(3)]
        self.ended = False

    def reset_count(self):
        self.tits_win = 0
        self.ass_win = 0
