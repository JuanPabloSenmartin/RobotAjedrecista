from urx import robotiq_two_finger_gripper
import time
import socket
import urx

# Conect to robot:
HOST = "192.168.0.18" # IP del robot
PORT = 30002 # port: 30001, 30002 o 30003, en ambos extremos

rob = urx.Robot(HOST)
robotiqgrip = robotiq_two_finger_gripper.Robotiq_Two_Finger_Gripper(rob)
print("conectando a gripper...")
time.sleep(1)


print("Conectando a IP: ", HOST)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("conectando...")
s.connect((HOST, PORT))
time.sleep(0.5)
print("Conectado con el robot")

urscript = robotiqgrip._get_new_urscript()

# rob.send_program(str(urscript._set_gripper_position(165)))
urscript._set_gripper_activate()

robotiqgrip.close_gripper()

robotiqgrip.open_gripper()