import socket
import sys
import time
import numpy as np
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

def init_robot():
    # Conexiones IP
    HOST = "192.168.0.18"  # IP del robot
    PORT = 30001  # port: 30001, 30002 o 30003, en ambos extremos
    print("Conectando a IP: ", HOST)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("conectando...")
    s.connect((HOST, PORT))
    time.sleep(0.5)
    return s


def init_gripper():
    rob = urx.Robot("192.168.0.18")
    robotiqgrip = Robotiq_Two_Finger_Gripper(rob)
    print("conectando a gripper...")
    time.sleep(1)
    return rob, robotiqgrip


class Cobot:
    FIXED_VELOCITY = 0.1
    ARBITRARY_ACCELERATION = 0.06

    GRIPPER_CLOSED = 200
    GRIPPER_SEMI_CLOSED = 100
    GRIPPER_OPEN = 0

    def __init__(self):
        self.robot_actual_position = [0.514, -0.2535]
        self.robot_actual_z = 0.12
        self.cobot = init_robot()
        self.rob, self.gripper = init_gripper()

    def init_position(self, position, z):
        # command = f"movel(p[{position[0]:.2f}, {position[1]:.2f}, {z:.2f}, 2.22, -2.22, 0], a={self.ARBITRARY_ACCELERATION:.2f}, v={self.FIXED_VELOCITY:.2f}, t={5:.2f})\n"
        command = f"movel(p[{position[0]:.2f}, {position[1]:.2f}, {z:.2f}, 2.89, -1.24, 0], a={self.ARBITRARY_ACCELERATION:.2f}, v={self.FIXED_VELOCITY:.2f}, t={4:.2f})\n"
        self.cobot.send(command.encode('utf-8'))
        print(f"Command sent: {command}")
        self.update_position(position, z)
        time.sleep(4)

    def update_position(self, position, z):
        self.robot_actual_position = position
        self.robot_actual_z = z

    # Calcula la distancia entre dos puntos
    def calculate_distance(self, x1, y1, x2, y2):
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Calcula el tiempo necesario para moverse entre dos puntos dado una velocidad fija
    def calculate_time(self, distance, velocity):
        return distance / velocity

    def move_robot(self, position, z):
        time_to_travel = self.get_time_to_travel(position, z)
        print(f"Time to travel: {time_to_travel}")
        command = f"movel(p[{position[0]:.2f}, {position[1]:.2f}, {z:.2f}, 2.89, -1.24, 0], a={self.ARBITRARY_ACCELERATION:.2f}, v={self.FIXED_VELOCITY:.2f}, t={time_to_travel:.2f})\n"
        # if t is None:
        #     command = f"movel(p[{position[0]:.2f}, {position[1]:.2f}, {z:.2f}, 2.22, -2.22, 0], a={self.ARBITRARY_ACCELERATION:.2f}, v={self.FIXED_VELOCITY:.2f})\n"
        # else:
        #     command = f"movel(p[{position[0]:.2f}, {position[1]:.2f}, {z:.2f}, 2.22, -2.22, 0], a={self.ARBITRARY_ACCELERATION:.2f}, v={self.FIXED_VELOCITY:.2f}, t={t:.2f})\n"
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
            return 2
        distance = self.calculate_distance(x1, y1, x2, y2)
        time_to_travel = self.calculate_time(distance, self.FIXED_VELOCITY)
        return time_to_travel + 1 if time_to_travel > 1 else 1

    def open_gripper(self):
        self.gripper.open_gripper()
        time.sleep(3)

    def close_gripper(self):
        self.gripper.close_gripper()
        time.sleep(1)

    def semi_open_gripper(self):
        self.gripper.gripper_action(120)
        time.sleep(1)

    def semiOpenGripper2(self, val):
        self.gripper.gripper_action(val)

    def stop_robot(self):
        self.cobot.close()
        sys.exit()
