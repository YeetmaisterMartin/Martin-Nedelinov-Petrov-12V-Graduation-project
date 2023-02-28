import PlayerVsPlayer as PvP
import pygame as p
import ChessEngine
import SmartMoveFinder
PINK = p.Color(235, 203, 197)
RED = p.Color(123, 24, 24)
COLORS = [PINK, RED]


def player_vs_computer_launcher():
    p.init()
    screen = p.display.set_mode((PvP.WIDTH, PvP.HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    sound = p.mixer.Sound("sounds/pick.wav")
    ai_sound = p.mixer.Sound("sounds/undo.wav")
    valid_moves = gs.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    PvP.load_images()
    running = True
    sq_selected = ()  # will keep track of last click of the user
    player_clicks = []  # keeps track of player clicks (two tuples: eg. [(6, 4), [4, 4]])
    game_over = False
    player_one = True
    player_two = False

    while running:
        human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

                # AI Move Finder
            if not game_over and not human_turn:
                ai_move = SmartMoveFinder.find_best_move_minmax(gs, valid_moves)
                ai_sound.play(loops=0)
                gs.make_move(ai_move)
                move_made = True
                human_turn = True
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    sound.play(loops=0)
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // PvP.SQ_SIZE
                    row = location[1] // PvP.SQ_SIZE
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

            if move_made:
                valid_moves = gs.get_valid_moves()
                move_made = False

            PvP.draw_game_state(screen, gs, valid_moves, sq_selected,COLORS)
            if gs.checkmate:
                game_over = True
                if gs.white_to_move:
                    PvP.draw_text(screen, "Computer wins by checkmate")
                else:
                    PvP.draw_text(screen, "you win by checkmate")

            elif gs.stalemate:
                game_over = True
                PvP.draw_text(screen, "Stalemate")

            clock.tick(15)
            p.display.flip()
