

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

    def reset(self):
        self._turn = 1
        self._p_index = 0
        self.board = [
            'kqbnr',
            'ppppp',
            '.....',
            '.....',
            'PPPPP',
            'RNBQK',
        ]

    def __init__(self):
        self.reset()

    def get_board(self):
        board_str = "\n".join(self.board)
        return "{} {}\n{}\n".format(self.turn, self.player, board_str)

    def set_board(self, state_str):
        header, board_str = state_str.split('\n', 1)
        self.turn, self.player = header.split()

        self.board = board_str.splitlines()

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

        pieces = "".join(self.board)

        if 'K' not in pieces:
            return 'B'
        if 'k' not in pieces:
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
