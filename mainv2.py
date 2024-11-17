import math
import sys
import time

# from RobotAjedrecista.Chess.chess_utils import Chess
from Cobot.cobot_utils import Cobot
import sys
import urx

from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

import socket
import sys
import time
import numpy as np
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

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

def hasChessboardChanged(chess, newBoard):
    return not(chess.areChessboardsEqual(newBoard))

def isMoveValid(chess, newBoard):
    return chess.isMoveValid(newBoard)

def stopRobot(cobot):
    cobot.move_robot(POSITION, z_HIGH)
    cobot.move_robot(INIT_POSITION, z_HIGH)
    cobot.stopRobot()


if __name__ == "__main__":
    HOST = "192.168.0.18"
    #
    #
    rob = urx.Robot(HOST)
    robotiqgrip = Robotiq_Two_Finger_Gripper(rob)
    print("conectando a gripper...")
    time.sleep(1)
    #
    #
    #
    print("abrir gripper")
    # robotiqgrip.open_gripper()
    robotiqgrip.gripper_action(100)
    # rob.send_program(robotiqgrip.ret_program_to_run())


    print("cerrar gripper")
    robotiqgrip.close_gripper()

    # cobot = Cobot()

    # rob = (urx.Robot("192.168.0.18"))
    # robotiqgrip = Robotiq_Two_Finger_Gripper(rob)
    # print("conectando a gripper...")
    # time.sleep(1)
    #
    # print('sending command')
    #
    # urscript = robotiqgrip._get_new_urscript()

    # rob.send_program(str(urscript._set_gripper_position(165)))
    # urscript._set_gripper_activate()

    # robotiqgrip.gripper_action(value=100)
    # rob.send_program(str(robotiqgrip.gripper_action(GRIPPER_CLOSED)))

    # robotiqgrip.close_gripper()
    # time.sleep(5)
    # robotiqgrip.gripper_action(200)

    # chess = Chess()
    # INIT_POSITION = [0.4, 0.3, z_HIGH]
    # POSITION = [0.4, 0.3, z_HIGH]
    # global position
    # inital_pos = POSITION
    # cobot.move_robot([0.5, 0.3], z_HIGH)
    # time.sleep(2)
    #
    # cobot.move_robot([0.5, 0.3], z_LOW)
    #
    # time.sleep(5)
    # print('close gripper')
    # cobot.closeGripper()
    # time.sleep(5)
    # print('open gripper')
    # cobot.openGripper()
    # time.sleep(5)
    # sys.exit(0)

    # cobot.closeGripper()

    # gripper.gripper_action(GRIPPER_CLOSED)
    # rob.send_program(str(gripper.gripper_action(GRIPPER_CLOSED)))
    # time.sleep(3)
    # gripper.gripper_action(GRIPPER_OPEN)
    # rob.send_program(str(gripper.gripper_action(GRIPPER_OPEN)))
    # time.sleep(3)

    # # OPEN GRIPPER
    # urscript = gripper._get_new_urscript()
    #
    # # rob.send_program(str(urscript._set_gripper_position(165)))
    # urscript._set_gripper_activate()
    #
    # gripper.gripper_action(value=0)

    # while True:
    #     ## deteccion de piezas
    #     newBoard = []
    #     if hasChessboardChanged(chess, newBoard):
    #         if not(isMoveValid(chess, newBoard)):
    #             print('INVALID MOVE')
    #             stopRobot(cobot)
    #
    #         # update MY board
    #         # check checkmate or draw
    #         # check best move
    #         # if i take piece, first move enemy piece, then mine
    #         # else move my piece
    #         movePiece(cobot, [], [])
    #     else:
    #         time.sleep(2)



