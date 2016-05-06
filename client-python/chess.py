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
    return board_state.eval()


def chess_moves():
    # with reference to the state of the game and return the possible moves - one example is given below -
    # note that a move has exactly 6 characters

    return board_state.moves()


def chess_movesShuffled():
    return board_state.moves_shuffled()


def chess_movesEvaluated():
    # with reference to the state of the game, determine the possible moves and sort them in order of an increasing evaluation score before returning them - note that you can call the chess_movesShuffled() function in here

    return board_state.evaluated_moves()


def chess_move(strIn):
    board_state.do_move(strIn)


def chess_moveRandom():
    # perform a random move and return it - one example output is given below -
    # note that you can call the chess_movesShuffled() function as well as the chess_move() function in here
    return board_state.move_random()


def chess_moveGreedy():
    # perform a greedy move and return it - one example output is given below -
    # note that you can call the chess_movesEvaluated() function as well as the chess_move() function in here
    return board_state.move_greedy()


def chess_moveNegamax(intDepth, intDuration):
    # perform a negamax move and return it - one example output is given below -
    # note that you can call the the other functions in here

    return 'a2-a3\n'


def chess_moveAlphabeta(intDepth, intDuration):
    # perform a alphabeta move and return it - one example output is given below -
    # note that you can call the the other functions in here

    return 'a2-a3\n'


def chess_undo():
    board_state.undo()
