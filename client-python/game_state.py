from random import shuffle
from time import time

COUNTER_MOD = 10

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


class Timeout(Exception):
    pass


class BoardState(object):
    # read-only internals
    _players = ['W', 'B']
    _cols = 'abcde'
    _rows = '654321'
    _p_index = _turn = 0
    board = history = None
    start = time_limit = time_counter = cached_time = 0


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
    def fwd_factor(self):
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
        return max(min(val, 10000), -10000)

    def alnum_to_xy(self, alnum):
        x, y = alnum
        return self.cols.index(x), self.rows.index(y)

    def xy_to_alnum(self, x, y):
        return "{}{}".format(self.cols[x], self.rows[y])

    def get_piece(self, x, y):
        return self.board[y][x]

    def set_piece(self, x, y, piece):
        self.board[y][x] = piece

    def parse_move(self, move_str):
        start, finish = move_str.splitlines()[0].split('-')
        s_x, s_y = self.alnum_to_xy(start)
        e_x, e_y = self.alnum_to_xy(finish)
        return s_x, s_y, e_x, e_y

    def do_move(self, move_str):

        # Verify legal move
        moves = self.moves()
        if move_str not in moves:
            raise ValueError('"%s" not a valid move\nMoves available: "%s"' % (move_str, moves))

        # Parse move string for start/end coordinates
        s_x, s_y, e_x, e_y = self.parse_move(move_str)

        piece = self.get_piece(s_x, s_y)
        other = self.get_piece(e_x, e_y)

        # Back up board state
        self.history.append((s_x, s_y, e_x, e_y, piece, other))

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

    def moves(self):
        moves = set()
        finder = MoveFinder(self)
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if self.is_own(col):
                    moves.update(finder.moves(x, y))

        finder.board = None
        del finder
        return list(moves)

    def undo(self):
        if self.history:
            s_x, s_y, e_x, e_y, piece, other = self.history.pop()
            self.set_piece(e_x, e_y, other)
            self.set_piece(s_x, s_y, piece)
            self.player = self.opponent
            if self.player == 'B':
                self.turn -= 1

    def moves_shuffled(self):
        moves = self.moves()
        shuffle(moves)
        return moves

    def evaluated_moves(self):
        evaluated = []
        moves = self.moves_shuffled()

        for move in moves:
            self.do_move(move)
            evaluated.append((self.eval(), move))
            self.undo()

        return [m[1] for m in sorted(evaluated, key=lambda x: x[0])]

    def move_random(self):
        for move in self.moves_shuffled():
            self.do_move(move)
            return move

    def move_greedy(self):
        for move in self.evaluated_moves():
            self.do_move(move)
            return move

    def check_time(self):
        self.time_counter += 1
        if self.time_counter % COUNTER_MOD == 0:
            self.cached_time = (time() - self.start) * 1000
            if self.cached_time >= self.time_limit:
                raise Timeout
        return self.cached_time

    def negamax(self, depth, timed=False):

        if timed:
            self.check_time()

        if depth <= 0 or self.winner() != '?':
            return self.eval()

        score = -99999
        for move in self.moves_shuffled():
            self.do_move(move)
            try:
                score = max(score, -self.negamax(depth - 1, timed=timed))
                self.undo()
            except Timeout:
                self.undo()
                raise

        return score

    def move_negamax(self, depth, timed=False):
        best = ''
        score = -99999

        for move in self.moves_shuffled():
            if timed:
                self.check_time()

            self.do_move(move)
            try:
                temp = -self.negamax(depth - 1, timed=timed)
                self.undo()
            except Timeout:
                self.undo()
                raise

            if temp > score:
                best = move
                score = temp

        return best

    def setup_timed(self, duration):
        self.time_limit = max(float(duration)/((41 - self.turn) * 2) - 10, 1)
        self.time_counter = self.cached_time = 0
        self.start = time()

    def cleanup_timed(self):
        self.time_limit = self.time_counter = self.cached_time = self.start = 0

    def timed_negamax(self, depth, duration):

        if depth > 0:
            return self.move_negamax(depth)

        best = ''
        depth = 1

        self.setup_timed(duration)
        try:
            while True:
                best = self.move_negamax(depth, timed=True)
                print('depth: {}, best: {}, counter: {}'.format(depth, best.strip(), self.time_counter))
                depth += 1
        except Timeout:
            pass

        print(self.time_limit)
        print(self.cached_time)
        print((time() - self.start) * 1000)
        self.cleanup_timed()
        return best

    def alphabeta(self, depth, alpha, beta):
        if depth == 0 or self.winner() != '?':
            return self.eval()

        score = -99999
        for move in self.evaluated_moves():
            self.do_move(move)
            score = max(score, -self.alphabeta(depth - 1, -beta, -alpha))
            self.undo()

            alpha = max(alpha, score)

            if alpha >= beta:
                # print('move=%s alpha=%s beta=%s' % (move.splitlines()[0], alpha, beta))
                break

        return score

    def move_alphabeta(self, depth):
        best = ''
        alpha = -99999
        beta = 99999

        for move in self.evaluated_moves():
            self.do_move(move)
            temp = -self.alphabeta(depth - 1, -beta, -alpha)
            # nm_score = -self.negamax(depth - 1)
            # if nm_score != temp:
            #     print('mv=%s ab=%s nm=%s' % (move.splitlines()[0], temp, nm_score))
            self.undo()

            if temp > alpha:
                best = move
                alpha = temp
        # print('score=%s move=%s' % (alpha, best))
        return best


class MoveFinder(object):

    def __init__(self, board):
        """
        :type board: BoardState
        """
        self.board = board

    def get_piece(self, x, y):
        return self.board.get_piece(x, y)

    def xy_to_alnum(self, x, y):
        return self.board.xy_to_alnum(x, y)

    def is_valid(self, x, y):
        return self.board.is_valid(x, y)

    def is_nothing(self, piece):
        return self.board.is_nothing(piece)

    def is_enemy(self, piece):
        return self.board.is_enemy(piece)

    def is_own(self, piece):
        return self.board.is_own(piece)

    def moves(self, x, y):
        piece = self.get_piece(x, y).lower()
        if piece == 'p':
            moves_iter = self._pawn_moves(x, y)
        elif piece == 'k':
            moves_iter = self._king_moves(x, y)
        elif piece == 'n':
            moves_iter = self._knight_moves(x, y)
        elif piece == 'r':
            moves_iter = self._rook_moves(x, y)
        elif piece == 'q':
            moves_iter = self._queen_moves(x, y)
        elif piece == 'b':
            moves_iter = self._bishop_moves(x, y)
        else:
            moves_iter = []

        for m in moves_iter:
            yield m

    def move_str(self, start, dest):
        return '{}-{}\n'.format(self.xy_to_alnum(*start), self.xy_to_alnum(*dest))

    def _pawn_moves(self, x, y):
        dy = self.board.fwd_factor

        if self.is_valid(x, y + dy) and self.is_nothing(self.get_piece(x, y + dy)):
            yield self.move_str((x, y), (x, y + dy))

        for dx in (-1, 1):
            if self.is_valid(x + dx, y + dy) and self.is_enemy(self.get_piece(x + dx, y + dy)):
                yield self.move_str((x, y), (x + dx, y + dy))

    def _king_moves(self, x, y):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:  # not moving
                    continue
                elif not self.is_valid(x + dx, y + dy):  # off the board
                    continue
                elif not self.is_own(self.get_piece(x + dx, y + dy)):  # empty or take-able
                    yield self.move_str((x, y), (x + dx, y + dy))

    def _knight_moves(self, x, y):
        coords = [
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1),
        ]

        for dx, dy in coords:
            if self.is_valid(x + dx, y + dy) and not self.is_own(self.get_piece(x + dx, y + dy)):
                yield self.move_str((x, y), (x + dx, y + dy))

    def _extend_direction(self, x, y, dx, dy):
        i = 1
        while self.is_valid(x + (dx * i), y + (dy * i)):
            yield i, self.get_piece(x + (dx * i), y + (dy * i))
            i += 1

    def _rook_moves(self, x, y):
        coords = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in coords:
            for i, piece in self._extend_direction(x, y, dx, dy):
                if not self.is_own(piece):
                    yield self.move_str((x, y), (x + (dx * i), y + (dy * i)))
                    if self.is_enemy(piece):
                        break
                else:
                    break

    def _queen_moves(self, x, y):
        for m in self._rook_moves(x, y):
            yield m
        for m in self._bishop_moves(x, y):
            yield m

    def _bishop_moves(self, x, y):
        diags = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        shifts = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in diags:
            for i, piece in self._extend_direction(x, y, dx, dy):
                if self.is_own(piece):
                    break
                else:
                    yield self.move_str((x, y), (x + (dx * i), y + (dy * i)))
                    if self.is_enemy(piece):
                        break

        for dx, dy in shifts:
            if self.is_valid(x + dx, y + dy) and self.is_nothing(self.get_piece(x + dx, y + dy)):
                yield self.move_str((x, y), (x + dx, y + dy))
