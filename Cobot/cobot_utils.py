import socket
import sys
import time
import numpy as np
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

HOST = "192.168.0.102"
PORT = 30001

INITIAL_POSITION = [0.514, -0.2535]
INITIAL_Z = 0.12

FIXED_VELOCITY = 0.25
ARBITRARY_ACCELERATION = 0.1

def init_robot():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting with cobot...")
    s.connect((HOST, PORT))
    time.sleep(0.5)
    print("Successfully connected with cobot!")
    return s


def init_gripper():
    rob = urx.Robot(HOST)
    robotiqgrip = Robotiq_Two_Finger_Gripper(rob, force=1, payload=0.5)
    print("connecting with gripper...")
    time.sleep(1)
    print("Successfully connected with gripper!")
    return robotiqgrip


class Cobot:
    def __init__(self):
        self.robot_actual_position = INITIAL_POSITION
        self.robot_actual_z = INITIAL_Z
        self.cobot = init_robot()
        self.gripper = init_gripper()

    def init_position(self, position, z):
        command = f"movel(p[{position[0]:.2f}, {position[1]:.2f}, {z:.2f}, 2.89, -1.24, 0], a={ARBITRARY_ACCELERATION:.2f}, v={FIXED_VELOCITY:.2f}, t={4:.2f})\n"
        self.cobot.send(command.encode('utf-8'))
        print(f"Command sent: {command}")
        self.update_position(position, z)
        time.sleep(4)

    def update_position(self, position, z):
        self.robot_actual_position = position
        self.robot_actual_z = z

    # Calculate distance between two points
    def calculate_distance(self, x1, y1, x2, y2):
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def move_robot(self, position, z):
        time_to_travel = self.get_time_to_travel(position, z)
        print(f"Time to travel: {time_to_travel}")
        command = f"movel(p[{position[0]:.2f}, {position[1]:.2f}, {z:.2f}, 2.89, -1.24, 0], a={ARBITRARY_ACCELERATION:.2f}, v={FIXED_VELOCITY:.2f}, t={time_to_travel:.2f})\n"
        self.cobot.send(command.encode('utf-8'))
        print(f"Command sent: {command}")
        self.update_position(position, z)
        time.sleep(time_to_travel)

    def get_time_to_travel(self, position, z):
        x1 = self.robot_actual_position[0]
        y1 = self.robot_actual_position[1]
        x2 = position[0]
        y2 = position[1]
        if x1 == x2 and y1 == y2 :
            if z == self.robot_actual_z:
                return 0.1
            return 1.3
        distance = self.calculate_distance(x1, y1, x2, y2)
        time_to_travel = distance / FIXED_VELOCITY
        return time_to_travel if time_to_travel > 1 else 1

    def close_gripper(self):
        self.gripper.close_gripper()
        # time.sleep(0.5)

    def open_gripper(self):
        self.gripper.gripper_action(120)
        # time.sleep(0.5)

    def stop_robot(self):
        self.cobot.close()
        sys.exit()
