import socket
import sys
import time
import numpy as np
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

# Connection parameters
HOST = "192.168.0.102"
PORT = 30001

# Robot default settings
INITIAL_POSITION = [0.047, -0.25]
INITIAL_Z = 0.12
FIXED_VELOCITY = 0.25
ARBITRARY_ACCELERATION = 0.1


def init_robot():
    """Initialize socket connection to the robot."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting with cobot...")
    s.connect((HOST, PORT))
    time.sleep(0.5)
    print("Successfully connected with cobot!")
    return s


def init_gripper():
    """Initialize gripper connection."""
    rob = urx.Robot(HOST)
    robot_gripper = Robotiq_Two_Finger_Gripper(rob, force=1, payload=0.5)
    print("Connecting with gripper...")
    time.sleep(1)
    print("Successfully connected with gripper!")
    return robot_gripper


def calculate_distance(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Cobot:
    def __init__(self):
        """Initialize the cobot and its components."""
        self.robot_actual_position = INITIAL_POSITION[:]
        self.robot_actual_z = INITIAL_Z
        self.cobot = init_robot()
        self.gripper = init_gripper()

    def init_position(self, position, z):
        """Move the cobot to its initial position."""
        self.move_robot(position, z, duration=4)

    def update_position(self, position, z):
        """Update the stored position of the robot."""
        self.robot_actual_position = position[:]
        self.robot_actual_z = z

    def move_robot(self, position, z, duration=None):
        """Move the robot to a specific position."""
        time_to_travel = duration if duration else self.get_time_to_travel(position, z)
        command = f"movel(p[{position[0]:.2f}, {position[1]:.2f}, {z:.2f}, 2.89, -1.24, 0], a={ARBITRARY_ACCELERATION:.2f}, v={FIXED_VELOCITY:.2f}, t={time_to_travel:.2f})\n"
        self.cobot.send(command.encode('utf-8'))
        self.update_position(position, z)
        time.sleep(time_to_travel)

    def get_time_to_travel(self, position, z):
        """Estimate the time required to reach the target position."""
        x1, y1 = self.robot_actual_position
        x2, y2 = position

        if (x1, y1) == (x2, y2):
            return 0.1 if z == self.robot_actual_z else 1.3

        distance = calculate_distance(x1, y1, x2, y2)
        return max(distance / FIXED_VELOCITY, 1)

    def close_gripper(self):
        """Close the gripper."""
        self.gripper.close_gripper()

    def open_gripper(self):
        """Open the gripper."""
        self.gripper.gripper_action(120)

    def stop_robot(self):
        """Close the connection and stop the robot."""
        self.cobot.close()
        sys.exit()