import random
import pygame as p
from Chess import ChessEngine, SmartMoveFinder
import time
from multiprocessing import Process, Queue

"""
This class will handle user input and display the current GameState object.
"""

p.init()
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 256
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    """
    Initialize a global dictionary of images. This will be called exactly once in the main
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chess-images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    """
    The main driver for our code. This will handle user input and update the graphics
    """
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    move_log_font = p.font.SysFont("Helvetica", 16, False, False)
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()

    move_made = False  # flag variable for when a move is made--
    # when an illegal move is made, we don't want to regenerate the list
    animate = False  # flag variable for animations

    load_images()
    running = True
    sq_selected = ()  # no sq selected (tuple: (row, col))
    player_clicks = []  # keep track of player clicks (two tuples: [(row1, col1), (row2, col2)]
    game_over = False

    ai_thinking = False
    move_finder_process = None
    move_undone = False

    player_one = False  # If a human is playing white, this will be true. If it's an AI playing white, it will be false
    player_two = True  # Same as above but for black

    while running:
        is_human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sq_selected == (row, col) or col >= 8:
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                    if len(player_clicks) == 2 and is_human_turn:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        print(move.get_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])  # valid_moves[i] accounts for
                                # en passant, pawn promotion; move does not
                                move_made = True
                                animate = True
                                sq_selected = ()
                                player_clicks = []
                            if not move_made:
                                player_clicks = [sq_selected]
                # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    gs.undo_move()
                    sq_selected = ()
                    player_clicks = []
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == p.K_r:  # resets game when r is pressed
                    gs = ChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

        # AI move finder
        if not game_over and not is_human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()
                move_finder_process = Process(target=SmartMoveFinder.find_best_move, args=(gs, valid_moves, return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:  # if there are no good moves, make a random one
                    ai_move = SmartMoveFinder.find_random_move(valid_moves)
                time.sleep(0.5)
                gs.make_move(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_valid_moves()
            move_made = False
            animate = False
            move_undone = False

        draw_game_state(screen, gs, valid_moves, sq_selected, move_log_font)

        if gs.checkmate or gs.stalemate or gs.is_three_move_repetition:
            game_over = True
            if gs.stalemate:
                text = 'Stalemate'
            elif gs.is_three_move_repetition:
                text = 'Three Move Repetition'
            else:
                text = 'Black wins by checkmate' if gs.white_to_move else 'White wins by checkmate'
            draw_end_game_text(screen, text)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, gs, valid_moves, sq_selected, move_log_font):
    """
    Responsible for all the graphics within a current game state
    """
    draw_board(screen)  # draws squares on the board
    highlight_squares(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)  # draws pieces on the board
    draw_move_log(screen, gs, move_log_font)


def highlight_squares(screen, gs, valid_moves, sq_selected):
    """
    Highlights the square selected and the possible moves for the piece selected
    """
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):  # ensure sqSelected is piece that can be moved
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value (0 transparent, 255 opaque)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


def draw_board(screen):
    """
    Draw the squares on the board
    """
    # TODO let the user choose the board color
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    """
    Draw the pieces on the board using the current GameState.board
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_move_log(screen, gs, font):
    """
    Draws the move log
    """
    padding = 5
    line_spacing = 2
    moves_per_row = 3

    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('Black'), move_log_rect)
    move_log = gs.move_log
    move_texts = []
    text_y = padding

    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + ". " + move_log[i].get_chess_notation() + " "
        if i + 1 < len(move_log):  # make sure black made a move
            move_string += move_log[i + 1].get_chess_notation()
        move_texts.append(move_string)

    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j] + " "
        text_object = font.render(text, True, p.Color('White'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def animate_move(move, screen, board, clock):
    """
    Animates the move made
    """
    global colors
    d_r = move.end_row - move.start_row  # delta row
    d_c = move.end_col - move.start_col
    frames_per_square = 10
    frame_count = (abs(d_r) + abs(d_c)) * frames_per_square
    for frame in range(frame_count + 1):
        r, c = (move.start_row + d_r * frame / frame_count, move.start_col + d_c * frame / frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        # erase piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = (move.end_row + 1) if move.piece_captured[0] == 'b' else (move.end_row - 1)
                end_square = p.Rect(move.end_col * SQ_SIZE, enpassant_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(600)


def draw_end_game_text(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, 0, p.Color('Gray'))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color('Black'))
    screen.blit(text_object, text_location.move(-2, -2))


if __name__ == "__main__":
    main()
