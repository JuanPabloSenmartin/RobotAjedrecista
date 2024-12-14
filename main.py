import time
from Chess.chess_utils import Chess
from Cobot.cobot_utils import Cobot
import keyboard

# z_high = 0.12
# z_low = 0.01
z_high = 0.12
z_low = 0.01

limit_y_left = 0 #valid is higher (+) than this
limit_x_down = 0.18 #valid is higher (+) than this

# init_position = [0.36, -0.04]
# position = [0.36, -0.04]
init_position = [0.514, -0.2535]
position = [0.514, -0.2535]

# [x,y,isOccupied]
outside_positions = []
outside_position_index = 0

chess = Chess()
cobot = Cobot()


map = {
 'h1': [0.5876, -0.091],   'h2': [0.5368, -0.091],   'h3': [0.486, -0.091],    'h4': [0.4352, -0.091],
 'h5': [0.3844, -0.091],   'h6': [0.3336, -0.091],   'h7': [0.2828, -0.091],   'h8': [0.232, -0.091],
 'g1': [0.5876, -0.1443],  'g2': [0.5368, -0.1443],  'g3': [0.486, -0.1443],   'g4': [0.4352, -0.1443],
 'g5': [0.3844, -0.1443],  'g6': [0.3336, -0.1443],  'g7': [0.2828, -0.1443],  'g8': [0.232, -0.1443],
 'f1': [0.5876, -0.1976],  'f2': [0.5368, -0.1976],  'f3': [0.486, -0.1976],   'f4': [0.4352, -0.1976],
 'f5': [0.3844, -0.1976],  'f6': [0.3336, -0.1976],  'f7': [0.2828, -0.1976],  'f8': [0.232, -0.1976],
 'e1': [0.5876, -0.2509],  'e2': [0.5368, -0.2509],  'e3': [0.486, -0.2509],   'e4': [0.4352, -0.2509],
 'e5': [0.3844, -0.2509],  'e6': [0.3336, -0.2509],  'e7': [0.2828, -0.2509],  'e8': [0.232, -0.2509],
 'd1': [0.5876, -0.3042],  'd2': [0.5368, -0.3042],  'd3': [0.486, -0.3042],   'd4': [0.4352, -0.3042],
 'd5': [0.3844, -0.3042],  'd6': [0.3336, -0.3042],  'd7': [0.2828, -0.3042],  'd8': [0.232, -0.3042],
 'c1': [0.5876, -0.3575],  'c2': [0.5368, -0.3575],  'c3': [0.486, -0.3575],   'c4': [0.4352, -0.3575],
 'c5': [0.3844, -0.3575],  'c6': [0.3336, -0.3575],  'c7': [0.2828, -0.3575],  'c8': [0.232, -0.3575],
 'b1': [0.5876, -0.4108],  'b2': [0.5368, -0.4108],  'b3': [0.486, -0.4108],   'b4': [0.4352, -0.4108],
 'b5': [0.3844, -0.4108],  'b6': [0.3336, -0.4108],  'b7': [0.2828, -0.4108],  'b8': [0.232, -0.4108],
 'a1': [0.5876, -0.4641],  'a2': [0.5368, -0.4641],  'a3': [0.486, -0.4641],   'a4': [0.4352, -0.4641],
 'a5': [0.3844, -0.4641],  'a6': [0.3336, -0.4641],  'a7': [0.2828, -0.4641],  'a8': [0.232, -0.4641]
}




height = {
    1: 0.01, #PAWN
    2: 0.01, #KNIGHT
    3: 0.02, #BISHOP
    4: 0.01, #ROOK
    5: 0.045, #QUEEN
    6: 0.045, #KING
}

def move(init_square, next_square, piece):
    init_pos = map.get(init_square)
    piece_height = height.get(piece)
    if next_square == 'OUT':
        next_pos = get_free_outside_position()
        drop_height = piece_height - 0.01
    else:
        next_pos = map.get(next_square)
        drop_height = None

    move_piece(init_pos, next_pos, piece_height, drop_height)

def move_piece(current_position, next_position, height_z_low, drop_height=None):
    cobot.semi_open_gripper()
    cobot.move_robot(current_position, z_high)
    cobot.move_robot(current_position, height_z_low)
    cobot.close_gripper()
    cobot.move_robot(current_position, z_high)
    cobot.move_robot(next_position, z_high)
    if drop_height is None:
        cobot.move_robot(next_position, height_z_low)
    else:
        cobot.move_robot(next_position, drop_height)
    # cobot.semiOpenGripper2(150)
    cobot.semi_open_gripper()
    cobot.move_robot(next_position, z_high)
    cobot.move_robot(init_position, z_high)
    global position
    position = [next_position[0], next_position[1], z_high]

def get_free_outside_position():
    global outside_positions
    global outside_position_index
    free_position = outside_positions[outside_position_index]
    outside_positions[outside_position_index] = [free_position[0], free_position[1], True]
    outside_position_index += 1
    return [free_position[0], free_position[1]]

def generate_outside_positions():
    dif = 0.05
    global outside_positions
    init_x = limit_x_down + (dif/2)
    y = limit_y_left + (dif / 2)
    x = init_x
    for l in range(4):
        for k in range(4):
            outside_positions.append([x, y, False])
            x += dif
        y += dif
        x = init_x

def print_game_over():
    print('GAME OVER')
    print("Reason for game over:")
    if chess.board.is_checkmate():
        print("Checkmate")
    elif chess.board.is_stalemate():
        print("Stalemate")
    elif chess.board.is_insufficient_material():
        print("Insufficient material")
    elif chess.board.is_seventy_five_moves():
        print("75-move rule")
    elif chess.board.is_fivefold_repetition():
        print("Fivefold repetition")

    result = chess.board.result()  # Get the result of the game
    # Determine the winner
    if result == "1-0":
        print("White wins!")
    elif result == "0-1":
        print("Black wins!")
    elif result == "1/2-1/2":
        print("It's a draw.")

def stop_robot():
    cobot.move_robot(position, z_high)
    cobot.move_robot(init_position, z_high)
    cobot.stop_robot()

#-191 wirst 3
if __name__ == "__main__":

    generate_outside_positions()

    cobot.init_position(init_position, z_high)

    # move('e3', 'e3', 3)

    # chess.board.set_fen('rnbqkbnr/ppppppp1/7p/4P3/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1')

    i = 0
    j = -1

    ##EXAMPLE
    aux_board = [  ## person WHITE, robot BLACK
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",  ## person: e2e4, robot: c7c5
        "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 1",  ## person: g1f3, robot: b8c6
        "r1bqkbnr/pp1ppppp/2n5/1Bp5/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 0 1",  ## person: f1b5, robot: g7g6
        "r1bqkbnr/pp1ppp1p/2n3p1/1Bp5/4P3/2N2N2/PPPP1PPP/R1BQK2R b KQkq - 0 1"  ## person: b1c3, robot: f8g7
    ]

    # new = "rnbqkbnr/ppp1ppp1/7p/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 1"

    while True:
        if i % 2 == 0:
            ## juega persona
            ## ESTO VA A SER BORRADO DESPUES, ES PARA MOCKEAR LOS MOVIMIENTOS DE LA PERSONA
            print("juega persona")
            j += 1
            i += 1
            continue

        ## detección de piezas
        ## ESTA VARIABLE TIENE QUE SER REEMPLAZADO POR EL FEN DEL ESTADO ACTUAL DEL TABLERO DETECTADO
        new_board = aux_board[j]

        is_chessboard_equal, person_move = chess.are_chessboards_equal(new_board)

        if not is_chessboard_equal:
            if not chess.is_move_valid(person_move):
                print('INVALID MOVE, STOPPING ROBOT: ', person_move)
                stop_robot()
                break
            else:
                chess.update_board(person_move)  # update MY board
                chess.print_board()

                # check checkmate or draw
                if chess.is_game_over():
                    print_game_over()
                    stop_robot()
                    break
                # check best move
                best_move = chess.find_best_move()
                # best_move = 'e5d6'
                print('best_move', best_move)

                if chess.is_move_valid(best_move):
                    from_square, to_square = chess.get_move_squares(best_move)
                    if chess.is_move_capture(best_move):
                        print('capture')
                        ##move captured piece first
                        move(to_square, 'OUT', chess.get_piece(to_square))

                    en_passant, captured_square = chess.is_move_en_passant(best_move)
                    if en_passant:
                        print('en passant')
                        print('captured square', captured_square)
                        ##move other piece first
                        move(captured_square, 'OUT', chess.get_piece(captured_square))

                    ##move piece
                    move(from_square, to_square, chess.get_piece(from_square))

                    if chess.is_move_promotion(best_move):
                        print('promotion')
                        ## TODO: Implement promotion logic
                        ##takes pawn out of the board
                        ##move()
                        ##brings queen back from outside the board
                        ##move()

                    if chess.is_move_castle(best_move):
                        print('castle')
                        ##move rook to new position
                        init_rook_square, next_rook_square = chess.get_castling_rook_positions(best_move)
                        move(init_rook_square, next_rook_square, chess.get_piece(init_rook_square))

                    chess.update_board(best_move)
                    chess.print_board()
                else:
                    print('invalid move made by stockfish')
        else:
            print('chessboards are equal')

        print("Press enter to continue...")
        keyboard.wait("space")
        i = i + 1