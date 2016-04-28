

class BoardState(object):
    # read-only internals
    _players = ['W', 'B']
    _cols = 'abcde'
    _rows = '654321'
    _p_index = _turn = 0
    board = None

    @property
    def players(self):
        return self._players

    @property
    def opponent(self):
        return self.players[self._p_index - 1]

    @property
    def player(self):
        return self.players[self._p_index]

    @player.setter
    def player(self, val):
        self._p_index = self.players.index(val)

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, val):
        self._turn = int(val)

    @property
    def board_str(self):
        return "\n".join(["".join(r) for r in self.board])

    @board_str.setter
    def board_str(self, val):
        self.board = [[c for c in r] for r in val.splitlines()]

    def reset(self):
        self._turn = 1
        self._p_index = 0
        self.board = [
            ['k', 'q', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K'],
        ]

    def __init__(self):
        self.reset()

    def get_board(self):
        return "{} {}\n{}\n".format(self.turn, self.player, self.board_str)

    def set_board(self, state_str):
        header, self.board_str = state_str.split('\n', 1)
        self.turn, self.player = header.split()

    def is_enemy(self, piece):
        return piece in PIECES[self.opponent]

    def is_own(self, piece):
        return piece in PIECES[self.player]

    @staticmethod
    def is_nothing(piece):
        if piece == '.':
            return True
        return False

    def winner(self):
        if self.turn > 40:
            return '='

        kings = set()
        for row in self.board:
            for col in row:
                if col == 'K':
                    kings.add('W')
                if col == 'k':
                    kings.add('B')
                if len(kings) >= 2:
                    return '?'
        if 'W' not in kings:
            return 'B'
        if 'B' not in kings:
            return 'W'
        return '?'

    @staticmethod
    def is_valid(x, y):
        return 0 <= x <= 4 and 0 <= y <= 5

    def eval(self):

        val = 0
        for row in self.board:
            for col in row:
                if self.is_own(col):
                    val += PIECE_VALUES[col.lower()]
                elif self.is_enemy(col):
                    val -= PIECE_VALUES[col.lower()]
        return val

    def alnum_to_xy(self, alnum):
        x, y = alnum
        return self.cols.index(x), self.rows.index(y)

    def xy_to_alnum(self, x, y):
        return "{}{}".format(self.cols[x], self.rows[y])

    def get_piece(self, x, y):
        return self.board[y][x]

    def set_piece(self, x, y, piece):
        self.board[y][x] = piece

    def do_move(self, move_str):
        start, finish = move_str.splitlines()[0].split('-')

        # get start piece by coordinates
        s_x, s_y = self.alnum_to_xy(start)
        assert self.is_valid(s_x, s_y)
        piece = self.get_piece(s_x, s_y)
        assert self.is_own(piece)

        # sanity check end coordinates
        e_x, e_y = self.alnum_to_xy(finish)
        assert self.is_valid(e_x, e_y)
        assert not self.is_own(self.get_piece(e_x, e_y))

        # Queenify pawns
        if e_y == 0 and piece == 'P':
            piece = 'Q'
        elif e_y == 5 and piece == 'p':
            piece = 'q'

        # Set new piece positions, update board state
        self.set_piece(e_x, e_y, piece)
        self.set_piece(s_x, s_y, '.')
        self.player = self.opponent
        if self.player == 'W':
            self.turn += 1


PIECE_VALUES = {
    'p': 100,
    'b': 300,
    'n': 300,
    'r': 500,
    'q': 900,
    'k': 10000,
}


PIECES = {
    'W': {'P', 'R', 'N', 'B', 'Q', 'K'},
    'B': {'k', 'q', 'b', 'n', 'r', 'p'},
}
