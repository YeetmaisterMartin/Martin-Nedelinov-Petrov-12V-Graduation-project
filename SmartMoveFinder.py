import random

# your king as it would be a checkmate before that happened
piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 1


def find_best_move_minmax(gs, valid_moves):
    global next_move
    next_move = None
    find_move_minmax(gs, valid_moves, DEPTH, gs.white_to_move)
    return next_move


def find_move_minmax(gs, valid_moves, depth, white_to_move):
    global next_move
    random.shuffle(valid_moves)
    if depth == 0:
        return score_material(gs.board)

    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_minmax(gs, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return max_score

    else:
        min_score = CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_minmax(gs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score


# A positive score good for white & a negative score good for black
def score_board(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE  # Black wins
        else:
            return CHECKMATE  # White wins
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':  # White material advantage is positive
                score += piece_score[square[1]]
            elif square[0] == 'b':  # Black material advantage is negative
                score -= piece_score[square[1]]

    return score


# Score the board based on material
def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':  # White material advantage is positive
                score += piece_score[square[1]]
            elif square[0] == 'b':  # Black material advantage is negative
                score -= piece_score[square[1]]

    return score
