

class BoardState(object):
    cols = 'abcde'
    rows = '654321'
    _turn = 1
    _player = 'W'
    _board = [
        'kqbnr',
        'ppppp',
        '.....',
        '.....',
        'PPPPP',
        'RNBQK',
    ]
    _black_pieces = {'k', 'q', 'b', 'n', 'r', 'p'}
    _white_pieces = {'P', 'R', 'N', 'B', 'Q', 'K'}
    turn = player = board = black_pieces = white_pieces = None

    def reset(self):
        self.turn = self._turn
        self.player = self._player
        self.board = self._board
        self.white_pieces = self._white_pieces
        self.black_pieces = self._black_pieces

    def __init__(self):
        self.reset()

    def get_board(self):
        board_str = "\n".join(self.board)
        return "{} {}\n{}\n".format(self.turn, self.player, board_str)

    def set_board(self, state_str):
        header, board_str = state_str.split('\n', 1)
        turn, self.player = header.split()
        self.turn = int(turn)

        self.white_pieces = set([c for c in board_str if c in self._white_pieces])
        self.black_pieces = set([c for c in board_str if c in self._black_pieces])

        self.board = board_str.splitlines()

    def is_enemy(self, piece):
        if self.player == 'W':
            return piece in self._black_pieces
        return piece in self._white_pieces

    def is_own(self, piece):
        if self.player == 'W':
            return piece in self._white_pieces
        return piece in self._black_pieces

    @staticmethod
    def is_nothing(piece):
        if piece == '.':
            return True
        return False

    def winner(self):
        if 'K' not in self.white_pieces:
            return 'B'
        if 'k' not in self.black_pieces:
            return 'W'
        if self.turn > 40:
            return '='
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
