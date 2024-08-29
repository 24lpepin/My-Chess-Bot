import random
# TODO see 1:27:00 ish for stuff to do

piece_value = {"K": 0, "Q": 9, "R": 5, "B": 3.1, "N": 2.9, "p": 1.1}
knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 1, 1, 0.2, 0.2, 0.2],
               [0.4, 0.25, 0.05, 0.1, 0.1, 0.05, 0.25, 0.4],
               [0.25, 0.2, 0.3, 0.0, 0.0, 0.3, 0.2, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

'''
Finds a random move
'''


def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


'''
Finds the best move based on material alone
'''


def find_greedy_move(gs, valid_moves):
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_min_max_score = CHECKMATE  # want to minimize the opponent's best move
    best_player_move = None
    for player_move in valid_moves:
        gs.make_move(player_move)
        opponent_moves = gs.get_valid_moves()
        if gs.stalemate:
            opponent_max_score = STALEMATE
        elif gs.checkmate:
            opponent_max_score = -CHECKMATE
        else:
            opponent_max_score = -CHECKMATE
            for opponent_move in opponent_moves:
                gs.make_move(opponent_move)
                gs.get_valid_moves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                elif gs.is_in_check:
                    score = -turn_multiplier * scoreMaterial(gs.board)
                else:
                    score = -turn_multiplier * scoreMaterial(gs.board)
                if score > opponent_max_score:
                    opponent_max_score = score
                gs.undo_move()
        if opponent_max_score < opponent_min_max_score:
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()
    return best_player_move


def find_best_move(gs, valid_moves, return_queue):
    """
    Helper method to make first recursive call
    """
    global next_move, counter
    next_move = None
    counter = 0
    # find_move_min_max(gs, valid_moves, DEPTH, gs.white_to_move)
    # find_move_nega_max(gs, valid_moves, DEPTH, 1 if gs.white_to_move else -1)
    find_move_nega_max_alpha_beta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.white_to_move else -1)
    print(counter)
    return_queue.put(next_move)


def find_move_min_max(gs, valid_moves, depth, white_to_move):
    global next_move, counter
    counter += 1
    if depth == 0:
        return scoreBoard(gs)

    if white_to_move:  # white to move => want to maximize score
        max_score = -CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs, next_moves, depth - 1, False)
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
            score = find_move_min_max(gs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score


def find_move_nega_max(gs, valid_moves, depth, turn_multiplier):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turn_multiplier * scoreBoard(gs)

    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max(gs, next_moves, depth - 1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
    return max_score


def find_move_nega_max_alpha_beta(gs, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turn_multiplier * scoreBoard(gs)

    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(gs, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
        if max_score > alpha:  # pruning
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def scoreBoard(gs):
    """
    Scores board based on material, piece activity, positioning, etc.
    """
    if gs.checkmate:
        if gs.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gs.stalemate:
        return STALEMATE
    elif gs.is_three_move_repetition:
        return STALEMATE

    score = 0
    score += get_doubled_pawns_score(gs)
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            piece = gs.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col] + (gs.num_moves ** 0.25) * 0.18
                if piece[0] == "w":
                    score += piece_value[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_value[piece[1]] + piece_position_score

    return score

def get_doubled_pawns_score(gs):
    doubled_pawns_value = 0.33
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            if col+1 < len(gs.board[row]):
                if gs.board[row][col] == gs.board[row][col+1] == "wp":
                    score -= doubled_pawns_value
                elif gs.board[row][col] == gs.board[row][col+1] == "bp":
                    score += doubled_pawns_value

    return score


def scoreMaterial(board):
    """
    Scores the board based on material
    """
    score = 0
    for r in board:
        for square in r:
            if square[0] == 'w':
                score += piece_value[square[1]]
            elif square[0] == 'b':
                score -= piece_value[square[1]]

    return score
