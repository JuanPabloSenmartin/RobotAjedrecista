
import logging
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'External-libraries' / 'python-urx-master'))
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

v = 0.8
a = 0.35

robot_startposition = (math.radians(-218),
                    math.radians(-63),
                    math.radians(-93),
                    math.radians(-20),
                    math.radians(90),
                    math.radians(0))
        
robot_reach_down_position = (math.radians(-218),
                    math.radians(-130),
                    math.radians(-75),
                    math.radians(-60),
                    math.radians(90),
                    math.radians(0))


def movejRobot(position):
    rob.movej(position, a, v, wait=True, relative=False, threshold=None)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)

    rob = urx.Robot("192.168.56.101")
    robotiqgrip = Robotiq_Two_Finger_Gripper(rob)
    #rob = urx.Robot("localhost")
    rob.set_tcp((0,0,0,0,0,0))
    rob.set_payload(0.5, (0,0,0))
    try:
        l = 0.05
        
        joint_angles = rob.getj()
        print('joint position: ', joint_angles)
        print('go to start position')
        movejRobot(robot_startposition)
        time.sleep(2)
        print('go down')
        movejRobot(robot_reach_down_position)
        time.sleep(2)
        print('close gripper')
        robotiqgrip.close_gripper()
        time.sleep(2)
        print('open gripper')
        robotiqgrip.open_gripper()
        print('go to start position')
        movejRobot(robot_startposition)  
        # print("robot tcp is at: ", pose)
        # print("absolute move in base coordinate ")
        # pose[2] += l
        # rob.movel(pose, acc=a, vel=v)
        # print("relative move in base coordinate ")
        # rob.translate((0, 0, -l), acc=a, vel=v)
        # print("relative move back and forth in tool coordinate")
        # rob.translate_tool((0, 0, -l), acc=a, vel=v)
        # rob.translate_tool((0, 0, l), acc=a, vel=v)
    finally:
        rob.close()