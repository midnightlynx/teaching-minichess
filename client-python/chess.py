import random


##########################################################
class Board(object):
    _turn = 1
    _player = 'W'
    _board = [
        ['k', 'q', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K'],
    ]
    turn = None
    player = None
    board = None

    def reset(self):
        self.turn = self._turn
        self.player = self._player
        self.board = self._board

    def __init__(self):
        self.reset()

    def get_board(self):
        board_str = "\n".join([''.join([c for c in row]) for row in self.board])
        return "{} {}\n{}\n".format(self.turn, self.player, board_str)

    def set_board(self, board_str):
        board = board_str.splitlines()
        turn, self.player = board[0].split()
        self.turn = int(turn)
        self.board = [[c for c in row] for row in board[1:]]


game_board = Board()

def chess_reset():
    game_board.reset()


def chess_boardGet():
    return game_board.get_board()


def chess_boardSet(strIn):
    game_board.set_board(strIn)


def chess_winner():
    # determine the winner of the current state of the game and return '?' or '=' or 'W' or 'B' -
    # note that we are returning a character and not a string

    return '?'


def chess_isValid(intX, intY):
    if intX < 0:
        return False

    elif intX > 4:
        return False

    if intY < 0:
        return False

    elif intY > 5:
        return False

    return True


def chess_isEnemy(strPiece):
    if strPiece == '.':
        return False
    return (game_board.player == 'W') != (strPiece == strPiece.upper())


def chess_isOwn(strPiece):
    if strPiece == '.':
        return False
    return (game_board.player == 'W') == (strPiece == strPiece.upper())


def chess_isNothing(strPiece):
    if strPiece == '.':
        return True
    return False


def chess_eval():
    # with reference to the state of the game, return the the evaluation score of the side on move -
    # note that positive means an advantage while negative means a disadvantage

    return 0


def chess_moves():
    # with reference to the state of the game and return the possible moves - one example is given below -
    # note that a move has exactly 6 characters

    strOut = []

    strOut.append('a2-a3\n')
    strOut.append('b2-b3\n')
    strOut.append('c2-c3\n')
    strOut.append('d2-d3\n')
    strOut.append('e2-e3\n')
    strOut.append('b1-a3\n')
    strOut.append('b1-c3\n')

    return strOut


def chess_movesShuffled():
    # with reference to the state of the game, determine the possible moves and shuffle them before returning them-
    # note that you can call the chess_moves() function in here

    return []


def chess_movesEvaluated():
    # with reference to the state of the game, determine the possible moves and sort them
    # in order of an increasing evaluation score before returning them -
    # note that you can call the chess_moves() function in here

    return []


def chess_move(strIn):
    # perform the supplied move (for example 'a5-a4\n') and update the state of the game / your internal variables
    # accordingly - note that it advised to do a sanity check of the supplied move

    pass


def chess_moveRandom():
    # perform a random move and return it - one example output is given below -
    # note that you can call the chess_movesShuffled() function as well as the chess_move() function in here

    return 'a2-a3\n'


def chess_moveGreedy():
    # perform a greedy move and return it - one example output is given below -
    # note that you can call the chess_movesEvaluated() function as well as the chess_move() function in here

    return 'a2-a3\n'


def chess_moveNegamax(intDepth, intDuration):
    # perform a negamax move and return it - one example output is given below -
    # note that you can call the the other functions in here

    return 'a2-a3\n'


def chess_moveAlphabeta(intDepth, intDuration):
    # perform a alphabeta move and return it - one example output is given below -
    # note that you can call the the other functions in here

    return 'a2-a3\n'


def chess_undo():
    # undo the last move and update the state of the game / your internal variables accordingly -
    # note that you need to maintain an internal variable that keeps track of the previous history for this

    pass
