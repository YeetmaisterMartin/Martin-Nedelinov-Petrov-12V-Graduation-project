import pygame as p
import ChessEngine

WIDTH = HEIGHT = 800
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
LIGHT_BLUE = p.Color(173, 216, 230)
BLUE = p.Color(0, 40, 139)
COLORS = [LIGHT_BLUE, BLUE]


def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def player_vs_player_launcher():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))

    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    sound = p.mixer.Sound("sounds/pick.wav")
    undo_sound = p.mixer.Sound("sounds/undo.wav")
    valid_moves = gs.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    load_images()
    running = True
    sq_selected = ()  # will keep track of last click of the user
    player_clicks = []  # keeps track of player clicks (two tuples: eg. [(6, 4), [4, 4]])
    game_over = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:  # When mouse is clicked
                sound.play(loops=0)
                if not game_over:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sq_selected == (row, col) or col >= 8:  # Clear clicks when the same square is clicked
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)  # Save click into playerClicks list
                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                move_made = True
                                sq_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]
            elif e.type == p.KEYDOWN:  # Key press handling
                if e.key == p.K_z:  # Press Z to undo a move
                    undo_sound.play(loops=0)
                    gs.undo_move()
                    move_made = True
                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    pass
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs, valid_moves, sq_selected, COLORS)

        if gs.checkmate:
            game_over = True
            if gs.white_to_move:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")

        elif gs.stalemate:
            game_over = True
            draw_text(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()


def highlight_squares(screen, gs, valid_moves, square_selected):
    # Highlight square selected and moves for piece selected.

    if square_selected != ():
        r, c = square_selected
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('yellow'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('green'))
            for m in valid_moves:
                if m.start_row == r and m.start_col == c:
                    screen.blit(s, (m.end_col * SQ_SIZE, m.end_row * SQ_SIZE))


def draw_game_state(screen, gs, valid_moves, square_selected, colors):
    draw_board(screen, colors)  # Draws the squares on the board
    highlight_squares(screen, gs, valid_moves, square_selected)  # highlight the squares
    draw_pieces(screen, gs.board)  # Draws pieces on top of those squares


def draw_board(screen, colors):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # Not an empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_text(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("grey"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                     HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))
