import math
import sys
import time
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
import socket
import numpy as np
from Chess.chess_utils import Chess
from Cobot.cobot_utils import Cobot
import keyboard

z_high = 0.12
z_low = 0.09

gripper_closed = 200
gripper_semi_closed = 100
gripper_open = 0

init_position = [0.4, 0.3, z_high]
position = [0.4, 0.3, z_high]

def move_piece(cobot, current_position, next_position):
    cobot.move_robot(current_position, z_high)
    time.sleep(5)
    cobot.move_robot(current_position, z_low)
    time.sleep(5)
    cobot.close_gripper()
    time.sleep(5)
    cobot.move_robot(current_position, z_high)
    time.sleep(5)
    cobot.move_robot(next_position, z_high)
    time.sleep(5)
    cobot.move_robot(next_position, z_low)
    time.sleep(5)
    cobot.open_gripper()
    time.sleep(5)
    cobot.move_robot(next_position, z_high)
    global position
    position = [next_position[0], next_position[1], z_high]

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


if __name__ == "__main__":
    # HOST = "192.168.0.18"
    # #
    # rob = urx.Robot(HOST)
    # robotiqgrip = Robotiq_Two_Finger_Gripper(rob)
    # print("conectando a gripper...")
    # time.sleep(1)
    # #
    # robotiqgrip.gripper_action(100)
    # print("cerrar gripper")
    # robotiqgrip.close_gripper()

    ####################################################################

    # cobot = Cobot()

    # INIT_POSITION = [0.4, 0.3, z_HIGH]
    # POSITION = [0.4, 0.3, z_HIGH]
    # global position
    # inital_pos = POSITION
    # cobot.move_robot([0.5, 0.3], z_HIGH)
    # time.sleep(2)
    #
    # cobot.move_robot([0.5, 0.3], z_LOW)

    ######################################################################

    chess = Chess()

    i = 0
    j = -1
    k = 0

    ##EXAMPLE
    aux_board = [  ## person WHITE, robot BLACK
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",  ## person: e2e4, robot: c7c5
        "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 1",  ## person: g1f3, robot: b8c6
        "r1bqkbnr/pp1ppppp/2n5/1Bp5/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 0 1",  ## person: f1b5, robot: g7g6
        "r1bqkbnr/pp1ppp1p/2n3p1/1Bp5/4P3/2N2N2/PPPP1PPP/R1BQK2R b KQkq - 0 1"  ## person: b1c3, robot: f8g7
    ]

    while True:
        if i % 2 == 0:
            ## juega persona
            ## ESTO VA A SER BORRADO DESPUES, ES PARA MOCKEAR LOS MOVIMIENTOS DE LA PERSONA
            print("juega persona")
            j += 1
            i += 1
            continue
        print("juega robot")

        ## detección de piezas
        ## ESTA VARIABLE TIENE QUE SER REEMPLAZADO POR EL FEN DEL ESTADO ACTUAL DEL TABLERO DETECTADO
        new_board = aux_board[j]

        is_chessboard_equal, move = are_chessboards_equal(chess, new_board)
        print('is_chessboard_equal', is_chessboard_equal)
        print('move', move)

        if not is_chessboard_equal:
            if not is_move_valid(chess, move):
                print('INVALID MOVE, STOPPING ROBOT: ', move)
                # stop_robot(cobot)
                break
            else:
                update_board(chess, move)  # update MY board
                chess.print_board()

                # check checkmate or draw
                if is_game_over(chess):
                    print_game_over(chess)
                    break
                # check best move
                best_move = find_best_move(chess)
                print('best_move', best_move)

                if is_move_valid(chess, best_move):

                    if is_capture(chess, best_move):
                        print('capture')
                        ##move other piece first
                        ##move_piece(cobot, [], [])

                    ##move piece
                    ##move_piece(cobot, [], [])

                    if is_promotion(chess, best_move):
                        print('promotion')
                        ##takes pawn out of the board
                        ##move_piece(cobot, [], [])
                        ##brings queen back from outside the board
                        ##move_piece(cobot, [], [])

                    if is_castle(chess, best_move):
                        print('castle')
                        ##move rook to new position
                        ##move_piece(cobot, [], [])

                    update_board(chess, best_move)
                    chess.print_board()
                else:
                    print('invalid move made by stockfish')
        else:
            print('chessboards are equal')

        print("Press enter to continue...")
        keyboard.wait("space")
        i = i + 1