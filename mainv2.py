import math
import sys
import time
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
import socket
import numpy as np
from Chess.chess_utils import Chess
import chess
from Cobot.cobot_utils import Cobot
import keyboard

# z_high = 0.12
# z_low = 0.01
z_high = 0.12
z_low = 0.01

limit_y_left = -0.08 #valid is higher (+) than this
limit_x_down = 0.17 #valid is higher (+) than this

# init_position = [0.36, -0.04]
# position = [0.36, -0.04]
init_position = [0.514, -0.2535]
position = [0.514, -0.2535]

outside_positions = [[0.25, 0]]
outside_position_index = 0

map = {
    'e1': [0.514, -0.2535],
    'e2': [0.465, -0.2535], #0.049
    'e3': [0.416, -0.2535],
    'e4': [0.367, -0.2535],
    'e5': [0.318, -0.2535],
    'e6': [0.269, -0.2535],
    'e7': [0.222, -0.2535],
    'e8': [0.171, -0.2535]
}

height = {
    chess.PAWN: 0.01,
    chess.ROOK: 0.01,
    chess.KNIGHT: 0.01,
    chess.BISHOP: 0.01,
    chess.QUEEN: 0.045,
    chess.KING: 0.045,
}

def move(cobot, init_square, next_square, piece):
    init_pos = map.get(init_square)
    piece_height = height.get(piece)
    if next_square == 'OUT':
        next_pos = getFreeOutsidePosition()
        drop_height = piece_height - 0.01
    else:
        next_pos = map.get(next_square)
        drop_height = None

    move_piece(cobot, init_pos, next_pos, piece_height, drop_height)

def move_piece(cobot, current_position, next_position, height_z_low, drop_height=None):
    cobot.semiOpenGripper()
    cobot.move_robot(current_position, z_high)
    # time.sleep(5)
    cobot.move_robot(current_position, height_z_low)
    cobot.closeGripper()
    cobot.move_robot(current_position, z_high)
    cobot.move_robot(next_position, z_high)
    time.sleep(10)
    if drop_height == None:
        cobot.move_robot(next_position, height_z_low)
    else:
        cobot.move_robot(next_position, drop_height)
    # cobot.semiOpenGripper2(150)
    cobot.semiOpenGripper()
    cobot.move_robot(next_position, z_high)
    cobot.move_robot(init_position, z_high)
    time.sleep(10)
    global position
    position = [next_position[0], next_position[1], z_high]

def getFreeOutsidePosition():
    ##TODO: IMPLEMENT LOGIC
    return outside_positions[0]

def generateOutsidePositions():
    dif = 0.05

def are_chessboards_equal(chess, new_board):
    return chess.are_chessboards_equal(new_board)

def is_move_valid(chess, move):
    return chess.is_move_valid(move)

def find_best_move(chess):
    return chess.find_best_move()

def update_board(chess, move):
    chess.move(move)

def is_game_over(chess):
    return chess.is_game_over()

def is_capture(chess, move):
    return chess.is_move_capture(move)

def is_castle(chess, move):
    return chess.is_move_castle(move)

def is_promotion(chess, move):
    return chess.is_move_promotion(move)

def print_game_over(chess):
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

def stop_robot(cobot):
    cobot.move_robot(position, z_high)
    cobot.move_robot(init_position, z_high)
    cobot.stop_robot()

#-191 wirst 3
if __name__ == "__main__":

    cobot = Cobot()

    # cobot.semiOpenGripper()
    # cobot.move_robot([0.5, -0.15], z_high)
    # cobot.move_robot([0.5, -0.15], z_low)
    # cobot.closeGripper()
    # cobot.move_robot([0.5, -0.15], z_high)
    # cobot.semiOpenGripper()
    # move_piece(cobot, [0.5, -0.15], [0.4, -0.15])
    move(cobot, 'e1', 'OUT', chess.ROOK)

    # ######################################################################
    #
    # chess = Chess()
    #
    # i = 0
    # j = -1
    # k = 0
    #
    # ##EXAMPLE
    # aux_board = [  ## person WHITE, robot BLACK
    #     "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",  ## person: e2e4, robot: c7c5
    #     "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 1",  ## person: g1f3, robot: b8c6
    #     "r1bqkbnr/pp1ppppp/2n5/1Bp5/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 0 1",  ## person: f1b5, robot: g7g6
    #     "r1bqkbnr/pp1ppp1p/2n3p1/1Bp5/4P3/2N2N2/PPPP1PPP/R1BQK2R b KQkq - 0 1"  ## person: b1c3, robot: f8g7
    # ]
    #
    # while True:
    #     if i % 2 == 0:
    #         ## juega persona
    #         ## ESTO VA A SER BORRADO DESPUES, ES PARA MOCKEAR LOS MOVIMIENTOS DE LA PERSONA
    #         print("juega persona")
    #         j += 1
    #         i += 1
    #         continue
    #     print("juega robot")
    #
    #     ## detección de piezas
    #     ## ESTA VARIABLE TIENE QUE SER REEMPLAZADO POR EL FEN DEL ESTADO ACTUAL DEL TABLERO DETECTADO
    #     new_board = aux_board[j]
    #
    #     is_chessboard_equal, move = are_chessboards_equal(chess, new_board)
    #     print('is_chessboard_equal', is_chessboard_equal)
    #     print('move', move)
    #
    #     if not is_chessboard_equal:
    #         if not is_move_valid(chess, move):
    #             print('INVALID MOVE, STOPPING ROBOT: ', move)
    #             # stop_robot(cobot)
    #             break
    #         else:
    #             update_board(chess, move)  # update MY board
    #             chess.print_board()
    #
    #             # check checkmate or draw
    #             if is_game_over(chess):
    #                 print_game_over(chess)
    #                 break
    #             # check best move
    #             best_move = find_best_move(chess)
    #             print('best_move', best_move)
    #
    #             if is_move_valid(chess, best_move):
    #
    #                 if is_capture(chess, best_move):
    #                     print('capture')
    #                     ##move other piece first
    #                     ##move_piece(cobot, [], [])
    #
    #                 ##move piece
    #                 ##move_piece(cobot, [], [])
    #
    #                 if is_promotion(chess, best_move):
    #                     print('promotion')
    #                     ##takes pawn out of the board
    #                     ##move_piece(cobot, [], [])
    #                     ##brings queen back from outside the board
    #                     ##move_piece(cobot, [], [])
    #
    #                 if is_castle(chess, best_move):
    #                     print('castle')
    #                     ##move rook to new position
    #                     ##move_piece(cobot, [], [])
    #
    #                 update_board(chess, best_move)
    #                 chess.print_board()
    #             else:
    #                 print('invalid move made by stockfish')
    #     else:
    #         print('chessboards are equal')
    #
    #     print("Press enter to continue...")
    #     keyboard.wait("space")
    #     i = i + 1