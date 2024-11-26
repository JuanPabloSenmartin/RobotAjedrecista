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

z_HIGH = 0.12
z_LOW = 0.09

GRIPPER_CLOSED = 200
GRIPPER_SEMI_CLOSED = 100
GRIPPER_OPEN = 0

INIT_POSITION = [0.4, 0.3, z_HIGH]
POSITION = [0.4, 0.3, z_HIGH]

def movePiece(cobot, currentPosition, nextPosition):
    cobot.move_robot(currentPosition, z_HIGH)
    time.sleep(5)
    cobot.move_robot(currentPosition, z_LOW)
    time.sleep(5)
    cobot.closeGripper()
    time.sleep(5)
    cobot.move_robot(currentPosition, z_HIGH)
    time.sleep(5)
    cobot.move_robot(nextPosition, z_HIGH)
    time.sleep(5)
    cobot.move_robot(nextPosition, z_LOW)
    time.sleep(5)
    cobot.openGripper()
    time.sleep(5)
    cobot.move_robot(nextPosition, z_HIGH)
    global position
    position = [nextPosition[0], nextPosition[1], z_HIGH]

def areChessboardsEqual(chess, newBoard):
    return chess.areChessboardsEqual(newBoard)

def findMoveMade(chess, newBoard):
    return not(chess.areChessboardsEqual(newBoard))

def isMoveValid(chess, move):
    return chess.isMoveValid(move)

def bestMove(chess):
    return chess.findBestMove()

def updateBoard(chess, move):
    chess.move (move)

def isGameOver(chess):
    return chess.isGameOver()

def isCapture(chess, move):
    return chess.isMoveCapture(move)

def isCastle(chess, move):
    return chess.isMoveCastle(move)

def isPromotion(chess, move):
    return chess.isMovePromotion(move)

def printGameOver(chess):
    print('GAME OVER')
    print("Reason for game over:")
    if chess.board.is_checkmate():
        print("Checkmate")
    elif chess.board.is_stalemate():
        print("Stalemate")
    elif chess.board.is_insufficient_material():
        print("Insufficient material")
    elif chess.board.is_seventyfive_moves():
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

def stopRobot(cobot):
    cobot.move_robot(POSITION, z_HIGH)
    cobot.move_robot(INIT_POSITION, z_HIGH)
    cobot.stopRobot()


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
    auxBoard = [ ## person WHITE, robot BLACK
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", ## person: e2e4, robot: c7c5
        "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 1", ## person: g1f3, robot: b8c6
        "r1bqkbnr/pp1ppppp/2n5/1Bp5/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 0 1", ## person: f1b5, robot: g7g6
        "r1bqkbnr/pp1ppp1p/2n3p1/1Bp5/4P3/2N2N2/PPPP1PPP/R1BQK2R b KQkq - 0 1" ## person: b1c3, robot: f8g7
    ]

    while True:
        if i%2 == 0:
            ## juega persona
            ## ESTO VA A SER BORRADO DESPUES, ES PARA MOCKEAR LOS MOVIMIENTOS DE LA PERSONA
            print("juega persona")
            j += 1
            i += 1
            continue
        print("juega robot")

        ## deteccion de piezas
        ## ESTA VARIABLE TIENE QUE SER REMPLAZADO POR EL FEN DEL ESTADO ACTUAL DEL TABLERO DETECTADO
        newBoard = auxBoard[j]

        isChessboardEqual, move = areChessboardsEqual(chess, newBoard)
        print('isChessboardEqual', isChessboardEqual)
        print('move', move)

        if not isChessboardEqual:
            if not isMoveValid(chess, move):
                print('INVALID MOVE, STOPPING ROBOT')
                print(move)
                # stopRobot(cobot)
                break
            else:
                print('valid move')
                updateBoard(chess, move) # update MY board
                print('board updated')

                chess.printBoard()

                # check checkmate or draw
                if isGameOver(chess):
                    printGameOver(chess)
                    break
                # check best move
                best_move = bestMove(chess)
                print('best_move', best_move)

                if isMoveValid(chess, best_move):

                    if isCapture(chess, best_move):
                        print('capture')
                        ##move other piece first
                        ##movePiece(cobot, [], [])

                    ##move piece
                    ##movePiece(cobot, [], [])

                    if isPromotion(chess, best_move):
                        print('promotion')
                        ##takes pawn out of the board
                        ##movePiece(cobot, [], [])
                        ##brings queen back from outside the board
                        ##movePiece(cobot, [], [])

                    if isCastle(chess, best_move):
                        print('castle')
                        ##move rook to new position
                        ##movePiece(cobot, [], [])

                    updateBoard(chess, best_move)
                    chess.printBoard()
                else:
                    print('invalid move made by stockfish')
        else:
            print('chessboards are equal')

        print("Press enter to continue...")
        keyboard.wait("space")
        i = i + 1