##########################################################

from game_state import BoardState

board_state = BoardState()


def chess_reset():
    board_state.reset()


def chess_boardGet():
    return board_state.get_board()


def chess_boardSet(strIn):
    board_state.set_board(strIn)


def chess_winner():
    return board_state.winner()


def chess_isValid(intX, intY):
    return board_state.is_valid(intX, intY)


def chess_isEnemy(strPiece):
    return board_state.is_enemy(strPiece)


def chess_isOwn(strPiece):
    return board_state.is_own(strPiece)


def chess_isNothing(strPiece):
    return board_state.is_nothing(strPiece)


def chess_eval():
    # with reference to the state of the game, return the the evaluation score of the side on move -
    # note that positive means an advantage while negative means a disadvantage

    return 0


def chess_moves():
    # with reference to the state of the game and return the possible moves - one example is given below -
    # note that a move has exactly 6 characters

    return ['a2-a3\n', 'b2-b3\n', 'c2-c3\n', 'd2-d3\n', 'e2-e3\n', 'b1-a3\n', 'b1-c3\n']


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
