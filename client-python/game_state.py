from copy import deepcopy
from random import shuffle


class BoardState(object):
    # read-only internals
    _players = ['W', 'B']
    _cols = 'abcde'
    _rows = '654321'
    _p_index = _turn = 0
    board = None
    history = None

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

    @property
    def _fwd_factor(self):
        return -1 if self.player == 'W' else 1

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
        self.history = []

    def __init__(self):
        self.reset()

    def get_board(self):
        return "{} {}\n{}\n".format(self.turn, self.player, self.board_str)

    def set_board(self, state_str):
        header, self.board_str = state_str.split('\n', 1)
        self.turn, self.player = header.split()
        self.history = []

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

        kings = set([c for r in self.board for c in r])

        if 'K' not in kings:
            return 'B'
        if 'k' not in kings:
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

        # Verify legal move
        assert move_str in self.moves()

        # Parse move string for start/end coordinates
        start, finish = move_str.splitlines()[0].split('-')
        s_x, s_y = self.alnum_to_xy(start)
        e_x, e_y = self.alnum_to_xy(finish)

        piece = self.get_piece(s_x, s_y)

        # Queenify pawns
        if e_y == 0 and piece == 'P':
            piece = 'Q'
        elif e_y == 5 and piece == 'p':
            piece = 'q'

        # Back up board state
        self.history.append(deepcopy(self.board))
        # Set new piece positions, update board state
        self.set_piece(e_x, e_y, piece)
        self.set_piece(s_x, s_y, '.')
        self.player = self.opponent
        if self.player == 'W':
            self.turn += 1

        return self.get_board()

    def moves(self):
        moves = []
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if self.is_own(col):
                    moves.extend(self._moves_by_piece(x, y))
        return moves

    def _moves_by_piece(self, x, y):
        piece = self.get_piece(x, y).lower()
        if piece == 'p':
            return self._pawn_moves(x, y)
        if piece == 'k':
            return self._king_moves(x, y)
        if piece == 'n':
            return self._knight_moves(x, y)
        if piece == 'r':
            return self._rook_moves(x, y)
        if piece == 'q':
            return self._queen_moves(x, y)
        if piece == 'b':
            return self._bishop_moves(x, y)
        return []

    def move_str(self, start, dest):
        return '{}-{}\n'.format(self.xy_to_alnum(*start), self.xy_to_alnum(*dest))

    def _pawn_moves(self, x, y):
        moves = []
        dy = self._fwd_factor

        if self.is_valid(x, y + dy) and self.is_nothing(self.get_piece(x, y + dy)):
            moves.append(self.move_str((x, y), (x, y + dy)))

        for dx in (-1, 1):
            if self.is_valid(x + dx, y + dy) and self.is_enemy(self.get_piece(x + dx, y + dy)):
                moves.append(self.move_str((x, y), (x + dx, y + dy)))

        return moves

    def _king_moves(self, x, y):
        moves = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:  # not moving
                    continue
                elif not self.is_valid(x + dx, y + dy):  # off the board
                    continue
                elif not self.is_own(self.get_piece(x + dx, y + dy)):  # empty or take-able
                    moves.append(self.move_str((x, y), (x + dx, y + dy)))
        return moves

    def _knight_moves(self, x, y):
        coords = [
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1),
        ]
        moves = []

        for dx, dy in coords:
            if self.is_valid(x + dx, y + dy) and not self.is_own(self.get_piece(x + dx, y + dy)):
                moves.append(self.move_str((x, y), (x + dx, y + dy)))
        return moves

    def _extend_direction(self, x, y, dx, dy):
        i = 1
        while self.is_valid(x + (dx * i), y + (dy * i)):
            yield i, self.get_piece(x + (dx * i), y + (dy * i))
            i += 1

    def _rook_moves(self, x, y):
        coords = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        moves = []

        for dx, dy in coords:
            for i, piece in self._extend_direction(x, y, dx, dy):
                if not self.is_own(piece):
                    moves.append(self.move_str((x, y), (x+(dx*i), y+(dy*i))))
                    if self.is_enemy(piece):
                        break
                else:
                    break
        return moves

    def _queen_moves(self, x, y):
        return list(set(self._rook_moves(x, y)) | set(self._bishop_moves(x, y)))

    def _bishop_moves(self, x, y):
        diags = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        shifts = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        moves = []

        for dx, dy in diags:
            for i, piece in self._extend_direction(x, y, dx, dy):
                if self.is_own(piece):
                    break
                else:
                    moves.append(self.move_str((x, y), (x+(dx*i), y+(dy*i))))
                    if self.is_enemy(piece):
                        break

        for dx, dy in shifts:
            if self.is_valid(x + dx, y + dy) and self.is_nothing(self.get_piece(x + dx, y + dy)):
                moves.append(self.move_str((x, y), (x + dx, y + dy)))

        return moves

    def undo(self):
        if self.history:
            self.board = self.history.pop()

    def moves_shuffled(self):
        moves = self.moves()
        shuffle(moves)
        return moves


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
